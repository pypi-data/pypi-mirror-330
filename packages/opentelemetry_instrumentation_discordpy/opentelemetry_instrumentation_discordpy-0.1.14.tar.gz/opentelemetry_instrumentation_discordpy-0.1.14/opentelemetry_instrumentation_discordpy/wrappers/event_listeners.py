"""
Instrumentation for discord.py event listeners
"""

import functools
import inspect
import logging
from typing import Any, Callable, Dict, Optional, cast

import discord
from discord.client import Client
from opentelemetry import trace
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import SpanKind, Status, StatusCode

logger = logging.getLogger(__name__)

# Original methods that we're wrapping
_WRAPPED_METHODS = {}

# List of events to instrument
DISCORD_EVENTS = [
    "on_message",
    "on_ready",
    "on_connect",
    "on_disconnect",
    "on_resumed",
    "on_error",
    "on_guild_join",
    "on_guild_remove",
    "on_member_join",
    "on_member_remove",
    "on_guild_channel_create",
    "on_guild_channel_delete",
    "on_guild_channel_update",
    "on_reaction_add",
    "on_reaction_remove",
    "on_interaction",
]

# Custom events registered by users
CUSTOM_EVENTS = set()


def _wrap_event_decorator(original_event: Callable) -> Callable:
    """
    Wrap the discord.Client.event decorator to trace event handlers.
    """
    @functools.wraps(original_event)
    def instrumented_event(coro: Callable) -> Callable:
        # Get the event name from the coroutine name
        event_name = coro.__name__

        # Only instrument events we're interested in or custom events
        if event_name not in DISCORD_EVENTS and event_name not in CUSTOM_EVENTS:
            return original_event(coro)

        @functools.wraps(coro)
        async def instrumented_coro(*args: Any, **kwargs: Any) -> Any:
            tracer = trace.get_tracer("discord.py.event")
            
            # Extract context information if available
            span_attributes = {}
            
            # Add guild information if available (for guild-related events)
            if len(args) > 1 and hasattr(args[1], "guild") and args[1].guild is not None:
                span_attributes["discord.guild.id"] = str(args[1].guild.id)
                span_attributes["discord.guild.name"] = args[1].guild.name
            
            # Add channel information if available
            if len(args) > 1 and hasattr(args[1], "channel"):
                span_attributes["discord.channel.id"] = str(args[1].channel.id)
                span_attributes["discord.channel.name"] = args[1].channel.name
                
            # Add author information for messages
            if event_name == "on_message" and len(args) > 1:
                message = args[1]
                span_attributes["discord.message.id"] = str(message.id)
                if hasattr(message, "author") and message.author is not None:
                    span_attributes["discord.author.id"] = str(message.author.id)
                    span_attributes["discord.author.name"] = str(message.author)
                span_attributes["discord.message.content_length"] = len(message.content) if hasattr(message, "content") else 0
            
            # Create a span for the event
            with tracer.start_as_current_span(
                f"{event_name}",
                kind=SpanKind.CONSUMER,
                attributes=span_attributes,
            ) as span:
                try:
                    result = await coro(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise

        # Call the original event decorator with our instrumented coroutine
        return original_event(instrumented_coro)

    return instrumented_event


def wrap_event_listeners() -> None:
    """
    Wrap discord.py event listeners with OpenTelemetry instrumentation.
    """
    logger.debug("Instrumenting discord.py event listeners")
    
    if getattr(Client, "event", None) is not None:
        _WRAPPED_METHODS[Client] = {}
        _WRAPPED_METHODS[Client]["event"] = Client.event
        Client.event = _wrap_event_decorator(Client.event)  # type: ignore


def register_custom_event(event_name: str) -> None:
    """
    Register a custom event to be instrumented.
    
    Args:
        event_name: The name of the event to register (e.g., "on_rabbitmq_message")
    """
    CUSTOM_EVENTS.add(event_name)
    logger.debug(f"Registered custom event: {event_name}")


def unregister_custom_event(event_name: str) -> None:
    """
    Unregister a custom event.
    
    Args:
        event_name: The name of the event to unregister
    """
    if event_name in CUSTOM_EVENTS:
        CUSTOM_EVENTS.remove(event_name)
        logger.debug(f"Unregistered custom event: {event_name}")


def unwrap_event_listeners() -> None:
    """
    Unwrap discord.py event listeners, removing OpenTelemetry instrumentation.
    """
    logger.debug("Removing instrumentation from discord.py event listeners")
    
    if Client in _WRAPPED_METHODS and "event" in _WRAPPED_METHODS[Client]:
        unwrap(Client, "event")
        _WRAPPED_METHODS[Client].pop("event")
        
    if not _WRAPPED_METHODS[Client]:
        _WRAPPED_METHODS.pop(Client)
