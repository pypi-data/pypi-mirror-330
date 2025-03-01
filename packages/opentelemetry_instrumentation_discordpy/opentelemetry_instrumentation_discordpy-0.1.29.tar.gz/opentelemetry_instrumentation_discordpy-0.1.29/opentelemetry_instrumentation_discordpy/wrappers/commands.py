"""
Instrumentation for discord.py commands
"""

import functools
import inspect
import logging
from typing import Any, Callable, Dict, Optional, cast

import discord
from discord.ext import commands
try:
    # Try to import app_commands for slash command support
    from discord import app_commands
    HAS_APP_COMMANDS = True
    logger.debug("Successfully imported discord.app_commands")
except ImportError:
    # app_commands might not be available in older discord.py versions
    app_commands = None
    HAS_APP_COMMANDS = False
    logger.debug("Could not import discord.app_commands, slash commands will not be instrumented")
from opentelemetry import trace
from opentelemetry.instrumentation.utils import unwrap
from opentelemetry.trace import SpanKind, Status, StatusCode

logger = logging.getLogger(__name__)

# Original methods that we're wrapping
_WRAPPED_METHODS = {}

def _wrap_app_command_invoke(original_func: Callable) -> Callable:
    """
    Wrap app_commands.Command._invoke to trace slash command invocation.
    """
    @functools.wraps(original_func)
    async def instrumented_app_command_invoke(*args: Any, **kwargs: Any) -> Any:
        command = args[0]
        interaction = args[1]
        params = args[2] if len(args) > 2 else kwargs.get("params", {})
        tracer = trace.get_tracer("discord.py.app_command")
        
        # Extract context information
        span_attributes = {
            "discord.app_command.name": command.name,
            "discord.app_command.type": str(getattr(command, "type", "unknown")),
            "discord.interaction.id": str(interaction.id),
            "discord.interaction.type": str(interaction.type),
        }
        
        # Add command path if available
        if hasattr(command, "qualified_name"):
            span_attributes["discord.app_command.qualified_name"] = command.qualified_name
        elif hasattr(command, "parent") and command.parent is not None:
            parent_name = getattr(command.parent, "name", "")
            span_attributes["discord.app_command.qualified_name"] = f"{parent_name} {command.name}".strip()
        
        # Add guild information if available
        if hasattr(interaction, "guild") and interaction.guild is not None:
            span_attributes["discord.guild.id"] = str(interaction.guild.id)
            span_attributes["discord.guild.name"] = interaction.guild.name
        elif hasattr(interaction, "guild_id") and interaction.guild_id is not None:
            span_attributes["discord.guild.id"] = str(interaction.guild_id)
        
        # Add channel information if available
        if hasattr(interaction, "channel") and interaction.channel is not None:
            span_attributes["discord.channel.id"] = str(interaction.channel.id)
            span_attributes["discord.channel.name"] = interaction.channel.name
        elif hasattr(interaction, "channel_id") and interaction.channel_id is not None:
            span_attributes["discord.channel.id"] = str(interaction.channel_id)
        
        # Add user information if available
        if hasattr(interaction, "user") and interaction.user is not None:
            span_attributes["discord.user.id"] = str(interaction.user.id)
            span_attributes["discord.user.name"] = str(interaction.user)
        
        # Add parameter information if available
        if params:
            try:
                # Convert params to a string representation
                params_str = str(params)
                if len(params_str) > 1000:
                    params_str = params_str[:997] + "..."
                span_attributes["discord.app_command.params"] = params_str
            except Exception as e:
                logger.warning(f"Error converting params to string: {e}")
        
        # Create a span for the slash command invocation
        with tracer.start_as_current_span(
            f"AppCommand.invoke.{span_attributes.get('discord.app_command.qualified_name', command.name)}",
            kind=SpanKind.CONSUMER,
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

    return instrumented_app_command_invoke


def _wrap_command_invoke(original_func: Callable) -> Callable:
    """
    Wrap Command.invoke to trace command invocation.
    """
    @functools.wraps(original_func)
    async def instrumented_invoke(*args: Any, **kwargs: Any) -> Any:
        command = args[0]
        ctx = args[1]
        tracer = trace.get_tracer("discord.py.command")
        
        # Extract context information
        span_attributes = {
            "discord.command.name": command.name,
            "discord.command.qualified_name": command.qualified_name,
        }
        
        # Add cog information if available
        if command.cog is not None:
            span_attributes["discord.command.cog"] = command.cog.__class__.__name__
        
        # Add guild information if available
        if hasattr(ctx, "guild") and ctx.guild is not None:
            span_attributes["discord.guild.id"] = str(ctx.guild.id)
            span_attributes["discord.guild.name"] = ctx.guild.name
        
        # Add channel information if available
        if hasattr(ctx, "channel"):
            span_attributes["discord.channel.id"] = str(ctx.channel.id)
            span_attributes["discord.channel.name"] = ctx.channel.name
        
        # Add author information if available
        if hasattr(ctx, "author") and ctx.author is not None:
            span_attributes["discord.author.id"] = str(ctx.author.id)
            span_attributes["discord.author.name"] = str(ctx.author)
        
        # Add message information if available
        if hasattr(ctx, "message") and ctx.message is not None:
            span_attributes["discord.message.id"] = str(ctx.message.id)
            if hasattr(ctx.message, "content"):
                span_attributes["discord.message.content_length"] = len(ctx.message.content)
        
        # Create a span for the command invocation
        with tracer.start_as_current_span(
            f"Command.invoke.{command.qualified_name}",
            kind=SpanKind.CONSUMER,
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

    return instrumented_invoke


def _wrap_cog_command_error(original_func: Callable) -> Callable:
    """
    Wrap Cog.cog_command_error to trace command errors.
    """
    @functools.wraps(original_func)
    async def instrumented_cog_command_error(*args: Any, **kwargs: Any) -> Any:
        cog = args[0]
        ctx = args[1]
        error = args[2]
        tracer = trace.get_tracer("discord.py.command")
        
        # Extract context information
        span_attributes = {
            "discord.cog.name": cog.__class__.__name__,
            "discord.error.type": error.__class__.__name__,
            "discord.error.message": str(error),
        }
        
        # Add command information if available
        if hasattr(ctx, "command") and ctx.command is not None:
            span_attributes["discord.command.name"] = ctx.command.name
            span_attributes["discord.command.qualified_name"] = ctx.command.qualified_name
        
        # Add guild information if available
        if hasattr(ctx, "guild") and ctx.guild is not None:
            span_attributes["discord.guild.id"] = str(ctx.guild.id)
            span_attributes["discord.guild.name"] = ctx.guild.name
        
        # Add channel information if available
        if hasattr(ctx, "channel"):
            span_attributes["discord.channel.id"] = str(ctx.channel.id)
            span_attributes["discord.channel.name"] = ctx.channel.name
        
        # Add author information if available
        if hasattr(ctx, "author") and ctx.author is not None:
            span_attributes["discord.author.id"] = str(ctx.author.id)
            span_attributes["discord.author.name"] = str(ctx.author)
        
        # Create a span for the command error
        with tracer.start_as_current_span(
            "Cog.cog_command_error",
            kind=SpanKind.CONSUMER,
            attributes=span_attributes,
        ) as span:
            try:
                if original_func is not None:
                    result = await original_func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                else:
                    # If there's no error handler, just record the error
                    span.set_status(Status(StatusCode.ERROR, str(error)))
                    return None
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    return instrumented_cog_command_error


def _wrap_process_commands(original_func: Callable) -> Callable:
    """
    Wrap Bot.process_commands to trace command processing.
    """
    @functools.wraps(original_func)
    async def instrumented_process_commands(*args: Any, **kwargs: Any) -> Any:
        bot = args[0]
        message = args[1]
        tracer = trace.get_tracer("discord.py.command")
        
        # Extract context information
        span_attributes = {}
        
        # Add message information if available
        if message is not None:
            span_attributes["discord.message.id"] = str(message.id)
            if hasattr(message, "content"):
                span_attributes["discord.message.content_length"] = len(message.content)
        
        # Add guild information if available
        if hasattr(message, "guild") and message.guild is not None:
            span_attributes["discord.guild.id"] = str(message.guild.id)
            span_attributes["discord.guild.name"] = message.guild.name
        
        # Add channel information if available
        if hasattr(message, "channel"):
            span_attributes["discord.channel.id"] = str(message.channel.id)
            span_attributes["discord.channel.name"] = message.channel.name
        
        # Add author information if available
        if hasattr(message, "author") and message.author is not None:
            span_attributes["discord.author.id"] = str(message.author.id)
            span_attributes["discord.author.name"] = str(message.author)
        
        # Create a span for the command processing
        with tracer.start_as_current_span(
            "Bot.process_commands",
            kind=SpanKind.CONSUMER,
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

    return instrumented_process_commands


def wrap_commands() -> None:
    """
    Wrap discord.py commands with OpenTelemetry instrumentation.
    """
    logger.debug("Instrumenting discord.py commands")
    
    # Wrap Command.invoke
    if hasattr(commands, "Command") and getattr(commands.Command, "invoke", None) is not None:
        if commands.Command not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[commands.Command] = {}
        _WRAPPED_METHODS[commands.Command]["invoke"] = commands.Command.invoke
        commands.Command.invoke = _wrap_command_invoke(commands.Command.invoke)  # type: ignore
    
    # Wrap Bot.process_commands
    if hasattr(commands, "Bot") and getattr(commands.Bot, "process_commands", None) is not None:
        if commands.Bot not in _WRAPPED_METHODS:
            _WRAPPED_METHODS[commands.Bot] = {}
        _WRAPPED_METHODS[commands.Bot]["process_commands"] = commands.Bot.process_commands
        commands.Bot.process_commands = _wrap_process_commands(commands.Bot.process_commands)  # type: ignore
    
    # Wrap Cog.cog_command_error for all existing cogs
    # This is more complex as we need to find all cog classes
    # We'll handle this by monkey patching the Cog.__init__ method
    original_cog_init = commands.Cog.__init__
    
    @functools.wraps(original_cog_init)
    def instrumented_cog_init(self, *args, **kwargs):
        # Call the original __init__
        original_cog_init(self, *args, **kwargs)
        
        # Check if this cog has a cog_command_error method
        if hasattr(self, "cog_command_error") and callable(self.cog_command_error):
            # Store the original method
            if self.__class__ not in _WRAPPED_METHODS:
                _WRAPPED_METHODS[self.__class__] = {}
            _WRAPPED_METHODS[self.__class__]["cog_command_error"] = self.cog_command_error
            
            # Replace with instrumented version
            self.cog_command_error = _wrap_cog_command_error(self.cog_command_error)
    
    # Replace the Cog.__init__ method
    commands.Cog.__init__ = instrumented_cog_init
    
    # Wrap app_commands (slash commands) if available
    if HAS_APP_COMMANDS and app_commands is not None:
        logger.debug("Instrumenting discord.py app_commands (slash commands)")
        
        # Wrap app_commands.Command._invoke
        if hasattr(app_commands, "Command") and hasattr(app_commands.Command, "_invoke"):
            if app_commands.Command not in _WRAPPED_METHODS:
                _WRAPPED_METHODS[app_commands.Command] = {}
            _WRAPPED_METHODS[app_commands.Command]["_invoke"] = app_commands.Command._invoke
            app_commands.Command._invoke = _wrap_app_command_invoke(app_commands.Command._invoke)
            logger.debug("Successfully wrapped app_commands.Command._invoke")
        else:
            logger.warning("Could not find app_commands.Command._invoke method")


def unwrap_commands() -> None:
    """
    Unwrap discord.py commands, removing OpenTelemetry instrumentation.
    """
    logger.debug("Removing instrumentation from discord.py commands")
    
    # Unwrap Command.invoke
    if hasattr(commands, "Command") and commands.Command in _WRAPPED_METHODS:
        for method_name, original_method in _WRAPPED_METHODS[commands.Command].items():
            setattr(commands.Command, method_name, original_method)
        _WRAPPED_METHODS.pop(commands.Command)
    
    # Unwrap Bot.process_commands
    if hasattr(commands, "Bot") and commands.Bot in _WRAPPED_METHODS:
        for method_name, original_method in _WRAPPED_METHODS[commands.Bot].items():
            setattr(commands.Bot, method_name, original_method)
        _WRAPPED_METHODS.pop(commands.Bot)
    
    # Restore original Cog.__init__
    if hasattr(commands, "Cog"):
        # We can't easily unwrap all cog instances, but we can stop wrapping new ones
        commands.Cog.__init__ = getattr(commands.Cog.__init__, "__wrapped__", commands.Cog.__init__)
    
    # Unwrap app_commands (slash commands) if available
    if HAS_APP_COMMANDS and app_commands is not None:
        logger.debug("Removing instrumentation from discord.py app_commands (slash commands)")
        
        # Unwrap app_commands.Command._invoke
        if hasattr(app_commands, "Command") and app_commands.Command in _WRAPPED_METHODS:
            for method_name, original_method in _WRAPPED_METHODS[app_commands.Command].items():
                setattr(app_commands.Command, method_name, original_method)
            _WRAPPED_METHODS.pop(app_commands.Command)
    
    # Clear the wrapped methods dictionary
    _WRAPPED_METHODS.clear()
