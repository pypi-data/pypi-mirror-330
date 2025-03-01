"""
Instrumentation for discord.py message operations
"""

import functools
import inspect
import logging
from typing import Any, Callable, Dict, Optional, cast

import discord
from discord.channel import TextChannel
from discord.message import Message
from opentelemetry import trace
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import SpanKind, Status, StatusCode

logger = logging.getLogger(__name__)

# Original methods that we're wrapping
_WRAPPED_METHODS = {}


def _wrap_send_message(original_func: Callable) -> Callable:
    """
    Wrap TextChannel.send to trace message sending operations.
    """
    @functools.wraps(original_func)
    async def instrumented_send(*args: Any, **kwargs: Any) -> Any:
        channel = args[0]
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {
            "discord.channel.id": str(channel.id),
            "discord.channel.name": channel.name,
        }
        
        # Add guild information if available
        if hasattr(channel, "guild") and channel.guild is not None:
            span_attributes["discord.guild.id"] = str(channel.guild.id)
            span_attributes["discord.guild.name"] = channel.guild.name
        
        # Add content length if content is provided
        if "content" in kwargs and kwargs["content"] is not None:
            span_attributes["discord.message.content_length"] = len(str(kwargs["content"]))
        
        # Create a span for the send operation
        with tracer.start_as_current_span(
            "TextChannel.send",
            kind=SpanKind.PRODUCER,
            attributes=span_attributes,
        ) as span:
            try:
                result = await original_func(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))
                # Add message ID to span
                if result is not None and hasattr(result, "id"):
                    span.set_attribute("discord.message.id", str(result.id))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return instrumented_send


def _wrap_edit_message(original_func: Callable) -> Callable:
    """
    Wrap Message.edit to trace message editing operations.
    """
    @functools.wraps(original_func)
    async def instrumented_edit(*args: Any, **kwargs: Any) -> Any:
        message = args[0]
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {
            "discord.message.id": str(message.id),
        }
        
        # Add channel information if available
        if hasattr(message, "channel"):
            span_attributes["discord.channel.id"] = str(message.channel.id)
            span_attributes["discord.channel.name"] = message.channel.name
        
        # Add guild information if available
        if hasattr(message, "guild") and message.guild is not None:
            span_attributes["discord.guild.id"] = str(message.guild.id)
            span_attributes["discord.guild.name"] = message.guild.name
        
        # Add author information if available
        if hasattr(message, "author") and message.author is not None:
            span_attributes["discord.author.id"] = str(message.author.id)
            span_attributes["discord.author.name"] = str(message.author)
        
        # Add content length if content is provided
        if "content" in kwargs and kwargs["content"] is not None:
            span_attributes["discord.message.content_length"] = len(str(kwargs["content"]))
        
        # Create a span for the edit operation
        with tracer.start_as_current_span(
            "Message.edit",
            kind=SpanKind.PRODUCER,
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

    return instrumented_edit


def _wrap_delete_message(original_func: Callable) -> Callable:
    """
    Wrap Message.delete to trace message deletion operations.
    """
    @functools.wraps(original_func)
    async def instrumented_delete(*args: Any, **kwargs: Any) -> Any:
        message = args[0]
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {
            "discord.message.id": str(message.id),
        }
        
        # Add channel information if available
        if hasattr(message, "channel"):
            span_attributes["discord.channel.id"] = str(message.channel.id)
            span_attributes["discord.channel.name"] = message.channel.name
        
        # Add guild information if available
        if hasattr(message, "guild") and message.guild is not None:
            span_attributes["discord.guild.id"] = str(message.guild.id)
            span_attributes["discord.guild.name"] = message.guild.name
        
        # Add author information if available
        if hasattr(message, "author") and message.author is not None:
            span_attributes["discord.author.id"] = str(message.author.id)
            span_attributes["discord.author.name"] = str(message.author)
        
        # Create a span for the delete operation
        with tracer.start_as_current_span(
            "Message.delete",
            kind=SpanKind.PRODUCER,
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

    return instrumented_delete


def _wrap_trigger_typing(original_func: Callable) -> Callable:
    """
    Wrap TextChannel.trigger_typing to trace typing indicator operations.
    """
    @functools.wraps(original_func)
    async def instrumented_trigger_typing(*args: Any, **kwargs: Any) -> Any:
        channel = args[0]
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {
            "discord.channel.id": str(channel.id),
            "discord.channel.name": channel.name,
        }
        
        # Add guild information if available
        if hasattr(channel, "guild") and channel.guild is not None:
            span_attributes["discord.guild.id"] = str(channel.guild.id)
            span_attributes["discord.guild.name"] = channel.guild.name
        
        # Create a span for the typing operation
        with tracer.start_as_current_span(
            "TextChannel.trigger_typing",
            kind=SpanKind.PRODUCER,
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

    return instrumented_trigger_typing


def _wrap_add_reaction(original_func: Callable) -> Callable:
    """
    Wrap Message.add_reaction to trace reaction operations.
    """
    @functools.wraps(original_func)
    async def instrumented_add_reaction(*args: Any, **kwargs: Any) -> Any:
        message = args[0]
        emoji = args[1] if len(args) > 1 else kwargs.get("emoji")
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {
            "discord.message.id": str(message.id),
        }
        
        # Add emoji information if available
        if emoji is not None:
            span_attributes["discord.reaction.emoji"] = str(emoji)
        
        # Add channel information if available
        if hasattr(message, "channel"):
            span_attributes["discord.channel.id"] = str(message.channel.id)
            span_attributes["discord.channel.name"] = message.channel.name
        
        # Add guild information if available
        if hasattr(message, "guild") and message.guild is not None:
            span_attributes["discord.guild.id"] = str(message.guild.id)
            span_attributes["discord.guild.name"] = message.guild.name
        
        # Create a span for the add reaction operation
        with tracer.start_as_current_span(
            "Message.add_reaction",
            kind=SpanKind.PRODUCER,
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

    return instrumented_add_reaction


def _wrap_remove_reaction(original_func: Callable) -> Callable:
    """
    Wrap Message.remove_reaction to trace reaction removal operations.
    """
    @functools.wraps(original_func)
    async def instrumented_remove_reaction(*args: Any, **kwargs: Any) -> Any:
        message = args[0]
        emoji = args[1] if len(args) > 1 else kwargs.get("emoji")
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {
            "discord.message.id": str(message.id),
        }
        
        # Add emoji information if available
        if emoji is not None:
            span_attributes["discord.reaction.emoji"] = str(emoji)
        
        # Add channel information if available
        if hasattr(message, "channel"):
            span_attributes["discord.channel.id"] = str(message.channel.id)
            span_attributes["discord.channel.name"] = message.channel.name
        
        # Add guild information if available
        if hasattr(message, "guild") and message.guild is not None:
            span_attributes["discord.guild.id"] = str(message.guild.id)
            span_attributes["discord.guild.name"] = message.guild.name
        
        # Create a span for the remove reaction operation
        with tracer.start_as_current_span(
            "Message.remove_reaction",
            kind=SpanKind.PRODUCER,
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

    return instrumented_remove_reaction


def _wrap_pin_message(original_func: Callable) -> Callable:
    """
    Wrap Message.pin to trace pin operations.
    """
    @functools.wraps(original_func)
    async def instrumented_pin(*args: Any, **kwargs: Any) -> Any:
        message = args[0]
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {
            "discord.message.id": str(message.id),
        }
        
        # Add channel information if available
        if hasattr(message, "channel"):
            span_attributes["discord.channel.id"] = str(message.channel.id)
            span_attributes["discord.channel.name"] = message.channel.name
        
        # Add guild information if available
        if hasattr(message, "guild") and message.guild is not None:
            span_attributes["discord.guild.id"] = str(message.guild.id)
            span_attributes["discord.guild.name"] = message.guild.name
        
        # Create a span for the pin operation
        with tracer.start_as_current_span(
            "Message.pin",
            kind=SpanKind.PRODUCER,
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

    return instrumented_pin


def _wrap_unpin_message(original_func: Callable) -> Callable:
    """
    Wrap Message.unpin to trace unpin operations.
    """
    @functools.wraps(original_func)
    async def instrumented_unpin(*args: Any, **kwargs: Any) -> Any:
        message = args[0]
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {
            "discord.message.id": str(message.id),
        }
        
        # Add channel information if available
        if hasattr(message, "channel"):
            span_attributes["discord.channel.id"] = str(message.channel.id)
            span_attributes["discord.channel.name"] = message.channel.name
        
        # Add guild information if available
        if hasattr(message, "guild") and message.guild is not None:
            span_attributes["discord.guild.id"] = str(message.guild.id)
            span_attributes["discord.guild.name"] = message.guild.name
        
        # Create a span for the unpin operation
        with tracer.start_as_current_span(
            "Message.unpin",
            kind=SpanKind.PRODUCER,
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

    return instrumented_unpin


def wrap_message_operations() -> None:
    """
    Wrap discord.py message operations with OpenTelemetry instrumentation.
    """
    logger.debug("Instrumenting discord.py message operations")
    
    # Wrap TextChannel.send
    if getattr(TextChannel, "send", None) is not None:
        if TextChannel not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[TextChannel] = {}
        _WRAPPED_METHODS[TextChannel]["send"] = TextChannel.send
        TextChannel.send = _wrap_send_message(TextChannel.send)  # type: ignore
    
    # Wrap Message.edit
    if getattr(Message, "edit", None) is not None:
        if Message not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[Message] = {}
        _WRAPPED_METHODS[Message]["edit"] = Message.edit
        Message.edit = _wrap_edit_message(Message.edit)  # type: ignore
    
    # Wrap Message.delete
    if getattr(Message, "delete", None) is not None:
        if Message not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[Message] = {}
        _WRAPPED_METHODS[Message]["delete"] = Message.delete
        Message.delete = _wrap_delete_message(Message.delete)  # type: ignore
    
    # Wrap TextChannel.trigger_typing
    if getattr(TextChannel, "trigger_typing", None) is not None:
        if TextChannel not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[TextChannel] = {}
        _WRAPPED_METHODS[TextChannel]["trigger_typing"] = TextChannel.trigger_typing
        TextChannel.trigger_typing = _wrap_trigger_typing(TextChannel.trigger_typing)  # type: ignore
    
    # Wrap Message.add_reaction
    if getattr(Message, "add_reaction", None) is not None:
        if Message not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[Message] = {}
        _WRAPPED_METHODS[Message]["add_reaction"] = Message.add_reaction
        Message.add_reaction = _wrap_add_reaction(Message.add_reaction)  # type: ignore
    
    # Wrap Message.remove_reaction
    if getattr(Message, "remove_reaction", None) is not None:
        if Message not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[Message] = {}
        _WRAPPED_METHODS[Message]["remove_reaction"] = Message.remove_reaction
        Message.remove_reaction = _wrap_remove_reaction(Message.remove_reaction)  # type: ignore
    
    # Wrap Message.pin
    if getattr(Message, "pin", None) is not None:
        if Message not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[Message] = {}
        _WRAPPED_METHODS[Message]["pin"] = Message.pin
        Message.pin = _wrap_pin_message(Message.pin)  # type: ignore
    
    # Wrap Message.unpin
    if getattr(Message, "unpin", None) is not None:
        if Message not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[Message] = {}
        _WRAPPED_METHODS[Message]["unpin"] = Message.unpin
        Message.unpin = _wrap_unpin_message(Message.unpin)  # type: ignore


def unwrap_message_operations() -> None:
    """
    Unwrap discord.py message operations, removing OpenTelemetry instrumentation.
    """
    logger.debug("Removing instrumentation from discord.py message operations")
    
    # Unwrap TextChannel methods
    if TextChannel in _WRAPPED_METHODS:
        for method_name, original_method in _WRAPPED_METHODS[TextChannel].items():
            unwrap(TextChannel, method_name)
        _WRAPPED_METHODS.pop(TextChannel)
    
    # Unwrap Message methods
    if Message in _WRAPPED_METHODS:
        for method_name, original_method in _WRAPPED_METHODS[Message].items():
            unwrap(Message, method_name)
        _WRAPPED_METHODS.pop(Message)
