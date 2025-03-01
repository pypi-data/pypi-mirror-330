"""
Instrumentation for discord.py HTTP requests
"""

import functools
import inspect
import logging
import time
from typing import Any, Callable, Dict, Optional, cast

import discord
from discord.http import HTTPClient, Route
from opentelemetry import trace
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import SpanKind, Status, StatusCode

logger = logging.getLogger(__name__)

# Original methods that we're wrapping
_WRAPPED_METHODS = {}


def _wrap_request(original_func: Callable) -> Callable:
    """
    Wrap HTTPClient.request to trace Discord API calls.
    """
    @functools.wraps(original_func)
    async def instrumented_request(*args: Any, **kwargs: Any) -> Any:
        http_client = args[0]
        route = args[1]
        tracer = trace.get_tracer("discord.py.http")
        
        # Extract context information
        span_attributes = {
            "http.method": route.method,
            "http.url": route.url,
            "http.route": route.path,
            "discord.api.endpoint": route.path,
        }
        
        # Add rate limit information if available
        if hasattr(http_client, "_global_over"):
            # Convert to bool to ensure it's a valid attribute type
            span_attributes["discord.ratelimit.global"] = bool(http_client._global_over)
        
        # Add bucket information if available
        # Check if the HTTPClient has the get_bucket method (older versions of discord.py)
        if hasattr(http_client, "get_bucket"):
            try:
                bucket = http_client.get_bucket(route)
                if bucket is not None:
                    span_attributes["discord.ratelimit.remaining"] = bucket.remaining
                    span_attributes["discord.ratelimit.limit"] = bucket.limit
                    if bucket.reset_time is not None:
                        span_attributes["discord.ratelimit.reset_after"] = max(0, bucket.reset_time - time.time())
            except Exception:
                # Ignore errors when trying to get bucket information
                pass
        
        # Create a span for the HTTP request
        with tracer.start_as_current_span(
            f"Discord.API.{route.method}.{route.path}",
            kind=SpanKind.CLIENT,
            attributes=span_attributes,
        ) as span:
            start_time = time.time()
            try:
                result = await original_func(*args, **kwargs)
                
                # Record the response time
                span.set_attribute("http.response_time_ms", (time.time() - start_time) * 1000)
                
                # Record rate limit headers if present in the response
                if hasattr(http_client, "rate_limit_remaining"):
                    span.set_attribute("discord.ratelimit.remaining", http_client.rate_limit_remaining)
                if hasattr(http_client, "rate_limit_reset"):
                    span.set_attribute("discord.ratelimit.reset_at", http_client.rate_limit_reset)
                if hasattr(http_client, "rate_limit_bucket"):
                    span.set_attribute("discord.ratelimit.bucket", http_client.rate_limit_bucket)
                
                span.set_status(Status(StatusCode.OK))
                return result
            except discord.HTTPException as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                span.set_attribute("http.status_code", e.status)
                span.set_attribute("discord.error.code", e.code)
                span.set_attribute("discord.error.text", e.text)
                raise
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return instrumented_request


def wrap_http() -> None:
    """
    Wrap discord.py HTTP client with OpenTelemetry instrumentation.
    """
    logger.debug("Instrumenting discord.py HTTP client")
    
    # Wrap HTTPClient.request
    if getattr(HTTPClient, "request", None) is not None:
        if HTTPClient not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[HTTPClient] = {}
        _WRAPPED_METHODS[HTTPClient]["request"] = HTTPClient.request
        HTTPClient.request = _wrap_request(HTTPClient.request)  # type: ignore


def unwrap_http() -> None:
    """
    Unwrap discord.py HTTP client, removing OpenTelemetry instrumentation.
    """
    logger.debug("Removing instrumentation from discord.py HTTP client")
    
    # Unwrap HTTPClient.request
    if HTTPClient in _WRAPPED_METHODS and "request" in _WRAPPED_METHODS[HTTPClient]:
        unwrap(HTTPClient, "request")
        _WRAPPED_METHODS[HTTPClient].pop("request")
        
    if not _WRAPPED_METHODS.get(HTTPClient, {}):
        _WRAPPED_METHODS.pop(HTTPClient, None)
