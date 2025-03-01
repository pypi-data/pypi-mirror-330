"""
Instrumentation for discord.py message operations
"""

import functools
import inspect
import logging
from typing import Any, Callable, Dict, Optional, cast

# Set up logger first
logger = logging.getLogger(__name__)

import discord
try:
    # Try importing from discord.channel (older versions)
    from discord.channel import TextChannel
except ImportError:
    try:
        # Try importing from discord.abc (newer versions)
        from discord.abc import Messageable as TextChannel
        logger.debug("Using discord.abc.Messageable as TextChannel")
    except ImportError:
        # Fallback to direct access
        TextChannel = getattr(discord, "TextChannel", None)
        if TextChannel is None:
            logger.warning("Could not import TextChannel class, will try to find it at runtime")
            # We'll try to find it at runtime in wrap_message_operations

try:
    from discord.message import Message
except ImportError:
    Message = getattr(discord, "Message", None)
    if Message is None:
        logger.warning("Could not import Message class, will try to find it at runtime")
from opentelemetry import trace
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import SpanKind, Status, StatusCode

# Original methods that we're wrapping
_WRAPPED_METHODS = {}


def _wrap_send_message(original_func: Callable) -> Callable:
    """
    Wrap TextChannel.send to trace message sending operations.
    """
    @functools.wraps(original_func)
    async def instrumented_send(*args: Any, **kwargs: Any) -> Any:
        obj = args[0]
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {}
        
        # Handle different types of objects that might be passed as the first argument
        # Check if it's a Context object (from discord.ext.commands)
        if hasattr(obj, "channel"):
            # It's likely a Context object
            channel = obj.channel
            if hasattr(channel, "id"):
                span_attributes["discord.channel.id"] = str(channel.id)
            if hasattr(channel, "name"):
                span_attributes["discord.channel.name"] = channel.name
            
            # Add guild information if available
            if hasattr(obj, "guild") and obj.guild is not None:
                span_attributes["discord.guild.id"] = str(obj.guild.id)
                span_attributes["discord.guild.name"] = obj.guild.name
            
            # Add author information if available
            if hasattr(obj, "author") and obj.author is not None:
                span_attributes["discord.author.id"] = str(obj.author.id)
                span_attributes["discord.author.name"] = str(obj.author)
        else:
            # It's likely a Channel object
            channel = obj
            try:
                if hasattr(channel, "id"):
                    span_attributes["discord.channel.id"] = str(channel.id)
                if hasattr(channel, "name"):
                    span_attributes["discord.channel.name"] = channel.name
                
                # Add guild information if available
                if hasattr(channel, "guild") and channel.guild is not None:
                    span_attributes["discord.guild.id"] = str(channel.guild.id)
                    span_attributes["discord.guild.name"] = channel.guild.name
            except Exception as e:
                logger.warning(f"Error extracting channel attributes: {e}")
        
        # Add content length and content if provided
        if "content" in kwargs and kwargs["content"] is not None:
            content = str(kwargs["content"])
            span_attributes["discord.message.content_length"] = len(content)
            # Include the actual content (truncate if too long)
            if len(content) > 1000:
                span_attributes["discord.message.content"] = content[:997] + "..."
            else:
                span_attributes["discord.message.content"] = content
        
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
        
        # Add content length and content if provided
        if "content" in kwargs and kwargs["content"] is not None:
            content = str(kwargs["content"])
            span_attributes["discord.message.content_length"] = len(content)
            # Include the actual content (truncate if too long)
            if len(content) > 1000:
                span_attributes["discord.message.content"] = content[:997] + "..."
            else:
                span_attributes["discord.message.content"] = content
        
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
        obj = args[0]
        tracer = trace.get_tracer("discord.py.message")
        
        # Extract context information
        span_attributes = {}
        
        # Handle different types of objects that might be passed as the first argument
        # Check if it's a Context object (from discord.ext.commands)
        if hasattr(obj, "channel"):
            # It's likely a Context object
            channel = obj.channel
            if hasattr(channel, "id"):
                span_attributes["discord.channel.id"] = str(channel.id)
            if hasattr(channel, "name"):
                span_attributes["discord.channel.name"] = channel.name
            
            # Add guild information if available
            if hasattr(obj, "guild") and obj.guild is not None:
                span_attributes["discord.guild.id"] = str(obj.guild.id)
                span_attributes["discord.guild.name"] = obj.guild.name
        else:
            # It's likely a Channel object
            channel = obj
            try:
                if hasattr(channel, "id"):
                    span_attributes["discord.channel.id"] = str(channel.id)
                if hasattr(channel, "name"):
                    span_attributes["discord.channel.name"] = channel.name
                
                # Add guild information if available
                if hasattr(channel, "guild") and channel.guild is not None:
                    span_attributes["discord.guild.id"] = str(channel.guild.id)
                    span_attributes["discord.guild.name"] = channel.guild.name
            except Exception as e:
                logger.warning(f"Error extracting channel attributes: {e}")
        
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
    
    # First try with the imported TextChannel
    channel_classes_to_wrap = []
    
    if TextChannel is not None and hasattr(TextChannel, "send"):
        logger.debug(f"Found TextChannel.send method: {TextChannel.send}")
        channel_classes_to_wrap.append(TextChannel)
    else:
        logger.warning("TextChannel.send method not found in imported class")
    
    # Try to find the Messageable ABC and its implementations
    try:
        import inspect
        
        # Check if discord.abc.Messageable exists
        if hasattr(discord, "abc") and hasattr(discord.abc, "Messageable"):
            messageable = discord.abc.Messageable
            logger.debug(f"Found discord.abc.Messageable: {messageable}")
            
            # If Messageable has a send method directly, wrap it
            if hasattr(messageable, "send") and callable(getattr(messageable, "send")):
                logger.debug(f"Found Messageable.send method: {messageable.send}")
                if messageable not in channel_classes_to_wrap:
                    channel_classes_to_wrap.append(messageable)
            
            # Find all classes that implement Messageable
            for name, obj in inspect.getmembers(discord):
                if inspect.isclass(obj) and issubclass(obj, messageable) and obj is not messageable:
                    if hasattr(obj, "send") and callable(getattr(obj, "send")):
                        logger.debug(f"Found Messageable implementation with send method: {name}")
                        if obj not in channel_classes_to_wrap:
                            channel_classes_to_wrap.append(obj)
            
            # Check discord.channel module for Messageable implementations
            if hasattr(discord, "channel"):
                for name, obj in inspect.getmembers(discord.channel):
                    if inspect.isclass(obj) and hasattr(obj, "__mro__") and messageable in obj.__mro__:
                        if hasattr(obj, "send") and callable(getattr(obj, "send")):
                            logger.debug(f"Found Messageable implementation in discord.channel: {name}")
                            if obj not in channel_classes_to_wrap:
                                channel_classes_to_wrap.append(obj)
        
        # Fallback: find any class with a send method
        if not channel_classes_to_wrap:
            logger.warning("No Messageable implementations found, falling back to searching for any class with send method")
            for name, obj in inspect.getmembers(discord):
                if inspect.isclass(obj) and hasattr(obj, "send") and callable(getattr(obj, "send")):
                    logger.debug(f"Found class with send method: {name}")
                    channel_classes_to_wrap.append(obj)
                
            # Also check discord.channel module
            if hasattr(discord, "channel"):
                for name, obj in inspect.getmembers(discord.channel):
                    if inspect.isclass(obj) and hasattr(obj, "send") and callable(getattr(obj, "send")):
                        logger.debug(f"Found class with send method in discord.channel: {name}")
                        if obj not in channel_classes_to_wrap:
                            channel_classes_to_wrap.append(obj)
            
            # Also check discord.abc module
            if hasattr(discord, "abc"):
                for name, obj in inspect.getmembers(discord.abc):
                    if inspect.isclass(obj) and hasattr(obj, "send") and callable(getattr(obj, "send")):
                        logger.debug(f"Found class with send method in discord.abc: {name}")
                        if obj not in channel_classes_to_wrap:
                            channel_classes_to_wrap.append(obj)
    except Exception as e:
        logger.error(f"Error while inspecting discord module: {e}")
        logger.exception("Detailed traceback:")
    
    # Wrap all found channel classes
    for channel_class in channel_classes_to_wrap:
        try:
            logger.debug(f"Attempting to wrap send method for class: {channel_class.__name__}")
            if channel_class not in _WRAPPED_METHODS:
                _WRAPPED_METHODS[channel_class] = {}
            _WRAPPED_METHODS[channel_class]["send"] = channel_class.send
            channel_class.send = _wrap_send_message(channel_class.send)  # type: ignore
            logger.debug(f"Successfully wrapped {channel_class.__name__}.send with {_wrap_send_message.__name__}")
        except Exception as e:
            logger.error(f"Error wrapping send method for class {channel_class.__name__}: {e}")
    
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
    
    # Unwrap all wrapped classes
    for cls, methods in list(_WRAPPED_METHODS.items()):
        logger.debug(f"Unwrapping methods for class: {cls.__name__ if hasattr(cls, '__name__') else cls}")
        for method_name, original_method in methods.items():
            try:
                logger.debug(f"Unwrapping {cls.__name__ if hasattr(cls, '__name__') else cls}.{method_name}")
                setattr(cls, method_name, original_method)
            except Exception as e:
                logger.error(f"Error unwrapping {method_name} for class {cls.__name__ if hasattr(cls, '__name__') else cls}: {e}")
        _WRAPPED_METHODS.pop(cls)
    
    # Clear the wrapped methods dictionary
    _WRAPPED_METHODS.clear()
