"""
Instrumentation for discord.py voice clients
"""

import functools
import inspect
import logging
import time
from typing import Any, Callable, Dict, Optional, cast

import discord
from discord.voice_client import VoiceClient
from opentelemetry import trace
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import SpanKind, Status, StatusCode

logger = logging.getLogger(__name__)

# Original methods that we're wrapping
_WRAPPED_METHODS = {}


def _wrap_voice_connect(original_func: Callable) -> Callable:
    """
    Wrap VoiceClient.connect to trace voice connection.
    """
    @functools.wraps(original_func)
    async def instrumented_connect(*args: Any, **kwargs: Any) -> Any:
        voice_client = args[0]
        tracer = trace.get_tracer("discord.py.voice")
        
        # Extract context information
        span_attributes = {}
        
        # Add channel information if available
        if hasattr(voice_client, "channel") and voice_client.channel is not None:
            span_attributes["discord.voice.channel.id"] = str(voice_client.channel.id)
            span_attributes["discord.voice.channel.name"] = voice_client.channel.name
        
        # Add guild information if available
        if hasattr(voice_client, "guild") and voice_client.guild is not None:
            span_attributes["discord.guild.id"] = str(voice_client.guild.id)
            span_attributes["discord.guild.name"] = voice_client.guild.name
        
        # Create a span for the voice connection
        with tracer.start_as_current_span(
            "VoiceClient.connect",
            kind=SpanKind.CLIENT,
            attributes=span_attributes,
        ) as span:
            start_time = time.time()
            try:
                result = await original_func(*args, **kwargs)
                
                # Record the connection time
                span.set_attribute("discord.voice.connect_time_ms", (time.time() - start_time) * 1000)
                
                # Add endpoint information if available
                if hasattr(voice_client, "endpoint"):
                    span.set_attribute("discord.voice.endpoint", voice_client.endpoint)
                
                # Add session ID if available
                if hasattr(voice_client, "session_id"):
                    span.set_attribute("discord.voice.session_id", voice_client.session_id)
                
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return instrumented_connect


def _wrap_voice_disconnect(original_func: Callable) -> Callable:
    """
    Wrap VoiceClient.disconnect to trace voice disconnection.
    """
    @functools.wraps(original_func)
    async def instrumented_disconnect(*args: Any, **kwargs: Any) -> Any:
        voice_client = args[0]
        tracer = trace.get_tracer("discord.py.voice")
        
        # Extract context information
        span_attributes = {}
        
        # Add channel information if available
        if hasattr(voice_client, "channel") and voice_client.channel is not None:
            span_attributes["discord.voice.channel.id"] = str(voice_client.channel.id)
            span_attributes["discord.voice.channel.name"] = voice_client.channel.name
        
        # Add guild information if available
        if hasattr(voice_client, "guild") and voice_client.guild is not None:
            span_attributes["discord.guild.id"] = str(voice_client.guild.id)
            span_attributes["discord.guild.name"] = voice_client.guild.name
        
        # Add session information if available
        if hasattr(voice_client, "session_id"):
            span_attributes["discord.voice.session_id"] = voice_client.session_id
        
        # Create a span for the voice disconnection
        with tracer.start_as_current_span(
            "VoiceClient.disconnect",
            kind=SpanKind.CLIENT,
            attributes=span_attributes,
        ) as span:
            try:
                result = await original_func(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return instrumented_disconnect


def _wrap_voice_play(original_func: Callable) -> Callable:
    """
    Wrap VoiceClient.play to trace audio playback.
    """
    @functools.wraps(original_func)
    def instrumented_play(*args: Any, **kwargs: Any) -> Any:
        voice_client = args[0]
        source = args[1]
        tracer = trace.get_tracer("discord.py.voice")
        
        # Extract context information
        span_attributes = {}
        
        # Add channel information if available
        if hasattr(voice_client, "channel") and voice_client.channel is not None:
            span_attributes["discord.voice.channel.id"] = str(voice_client.channel.id)
            span_attributes["discord.voice.channel.name"] = voice_client.channel.name
        
        # Add guild information if available
        if hasattr(voice_client, "guild") and voice_client.guild is not None:
            span_attributes["discord.guild.id"] = str(voice_client.guild.id)
            span_attributes["discord.guild.name"] = voice_client.guild.name
        
        # Add audio source information if available
        if hasattr(source, "title"):
            span_attributes["discord.voice.audio.title"] = source.title
        if hasattr(source, "duration"):
            span_attributes["discord.voice.audio.duration"] = source.duration
        
        # Create a span for the audio playback
        with tracer.start_as_current_span(
            "VoiceClient.play",
            kind=SpanKind.PRODUCER,
            attributes=span_attributes,
        ) as span:
            try:
                result = original_func(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return instrumented_play


def _wrap_voice_pause(original_func: Callable) -> Callable:
    """
    Wrap VoiceClient.pause to trace audio pause.
    """
    @functools.wraps(original_func)
    def instrumented_pause(*args: Any, **kwargs: Any) -> Any:
        voice_client = args[0]
        tracer = trace.get_tracer("discord.py.voice")
        
        # Extract context information
        span_attributes = {}
        
        # Add channel information if available
        if hasattr(voice_client, "channel") and voice_client.channel is not None:
            span_attributes["discord.voice.channel.id"] = str(voice_client.channel.id)
            span_attributes["discord.voice.channel.name"] = voice_client.channel.name
        
        # Add guild information if available
        if hasattr(voice_client, "guild") and voice_client.guild is not None:
            span_attributes["discord.guild.id"] = str(voice_client.guild.id)
            span_attributes["discord.guild.name"] = voice_client.guild.name
        
        # Create a span for the audio pause
        with tracer.start_as_current_span(
            "VoiceClient.pause",
            kind=SpanKind.PRODUCER,
            attributes=span_attributes,
        ) as span:
            try:
                result = original_func(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return instrumented_pause


def _wrap_voice_resume(original_func: Callable) -> Callable:
    """
    Wrap VoiceClient.resume to trace audio resume.
    """
    @functools.wraps(original_func)
    def instrumented_resume(*args: Any, **kwargs: Any) -> Any:
        voice_client = args[0]
        tracer = trace.get_tracer("discord.py.voice")
        
        # Extract context information
        span_attributes = {}
        
        # Add channel information if available
        if hasattr(voice_client, "channel") and voice_client.channel is not None:
            span_attributes["discord.voice.channel.id"] = str(voice_client.channel.id)
            span_attributes["discord.voice.channel.name"] = voice_client.channel.name
        
        # Add guild information if available
        if hasattr(voice_client, "guild") and voice_client.guild is not None:
            span_attributes["discord.guild.id"] = str(voice_client.guild.id)
            span_attributes["discord.guild.name"] = voice_client.guild.name
        
        # Create a span for the audio resume
        with tracer.start_as_current_span(
            "VoiceClient.resume",
            kind=SpanKind.PRODUCER,
            attributes=span_attributes,
        ) as span:
            try:
                result = original_func(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return instrumented_resume


def _wrap_voice_stop(original_func: Callable) -> Callable:
    """
    Wrap VoiceClient.stop to trace audio stop.
    """
    @functools.wraps(original_func)
    def instrumented_stop(*args: Any, **kwargs: Any) -> Any:
        voice_client = args[0]
        tracer = trace.get_tracer("discord.py.voice")
        
        # Extract context information
        span_attributes = {}
        
        # Add channel information if available
        if hasattr(voice_client, "channel") and voice_client.channel is not None:
            span_attributes["discord.voice.channel.id"] = str(voice_client.channel.id)
            span_attributes["discord.voice.channel.name"] = voice_client.channel.name
        
        # Add guild information if available
        if hasattr(voice_client, "guild") and voice_client.guild is not None:
            span_attributes["discord.guild.id"] = str(voice_client.guild.id)
            span_attributes["discord.guild.name"] = voice_client.guild.name
        
        # Create a span for the audio stop
        with tracer.start_as_current_span(
            "VoiceClient.stop",
            kind=SpanKind.PRODUCER,
            attributes=span_attributes,
        ) as span:
            try:
                result = original_func(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return instrumented_stop


def wrap_voice() -> None:
    """
    Wrap discord.py voice client with OpenTelemetry instrumentation.
    """
    logger.debug("Instrumenting discord.py voice client")
    
    # Wrap VoiceClient.connect
    if getattr(VoiceClient, "connect", None) is not None:
        if VoiceClient not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[VoiceClient] = {}
        _WRAPPED_METHODS[VoiceClient]["connect"] = VoiceClient.connect
        VoiceClient.connect = _wrap_voice_connect(VoiceClient.connect)  # type: ignore
    
    # Wrap VoiceClient.disconnect
    if getattr(VoiceClient, "disconnect", None) is not None:
        if VoiceClient not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[VoiceClient] = {}
        _WRAPPED_METHODS[VoiceClient]["disconnect"] = VoiceClient.disconnect
        VoiceClient.disconnect = _wrap_voice_disconnect(VoiceClient.disconnect)  # type: ignore
    
    # Wrap VoiceClient.play
    if getattr(VoiceClient, "play", None) is not None:
        if VoiceClient not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[VoiceClient] = {}
        _WRAPPED_METHODS[VoiceClient]["play"] = VoiceClient.play
        VoiceClient.play = _wrap_voice_play(VoiceClient.play)  # type: ignore
    
    # Wrap VoiceClient.pause
    if getattr(VoiceClient, "pause", None) is not None:
        if VoiceClient not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[VoiceClient] = {}
        _WRAPPED_METHODS[VoiceClient]["pause"] = VoiceClient.pause
        VoiceClient.pause = _wrap_voice_pause(VoiceClient.pause)  # type: ignore
    
    # Wrap VoiceClient.resume
    if getattr(VoiceClient, "resume", None) is not None:
        if VoiceClient not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[VoiceClient] = {}
        _WRAPPED_METHODS[VoiceClient]["resume"] = VoiceClient.resume
        VoiceClient.resume = _wrap_voice_resume(VoiceClient.resume)  # type: ignore
    
    # Wrap VoiceClient.stop
    if getattr(VoiceClient, "stop", None) is not None:
        if VoiceClient not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[VoiceClient] = {}
        _WRAPPED_METHODS[VoiceClient]["stop"] = VoiceClient.stop
        VoiceClient.stop = _wrap_voice_stop(VoiceClient.stop)  # type: ignore


def unwrap_voice() -> None:
    """
    Unwrap discord.py voice client, removing OpenTelemetry instrumentation.
    """
    logger.debug("Removing instrumentation from discord.py voice client")
    
    # Unwrap VoiceClient methods
    if VoiceClient in _WRAPPED_METHODS:
        for method_name, original_method in _WRAPPED_METHODS[VoiceClient].items():
            unwrap(VoiceClient, method_name)
        _WRAPPED_METHODS.pop(VoiceClient)
