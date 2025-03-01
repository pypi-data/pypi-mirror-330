"""
Decorators for manual instrumentation of discord.py bots
"""

import functools
import inspect
import logging
import asyncio
from typing import Any, Callable, Dict, Optional, Union, cast

import discord
from discord.ext import commands
from opentelemetry import trace as trace_api
from opentelemetry.trace import SpanKind, Status, StatusCode

logger = logging.getLogger(__name__)


def trace(
    name: Optional[str] = None,
    attributes: Optional[Dict[str, str]] = None,
    kind: SpanKind = SpanKind.INTERNAL,
) -> Callable:
    """
    Decorator for tracing discord.py commands and event handlers.
    
    Args:
        name: Optional name for the span. If not provided, the function name will be used.
        attributes: Optional attributes to add to the span.
        kind: The kind of span to create. Defaults to SpanKind.INTERNAL.
    
    Returns:
        A decorator function that wraps the original function with tracing.
    
    Example:
        ```python
        @bot.command()
        @trace(name="my_command", attributes={"custom.attribute": "value"})
        async def my_command(ctx):
            await ctx.send("Hello, world!")
        ```
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get the tracer
            tracer = trace_api.get_tracer("discord.py.manual")
            
            # Determine the span name
            span_name = name if name is not None else func.__name__
            
            # Extract context information if available
            span_attributes = {}
            
            # Add custom attributes if provided
            if attributes is not None:
                span_attributes.update(attributes)
            
            # Try to extract context from args if it's a command
            ctx = None
            if len(args) > 0:
                # Check if first arg is a commands.Context
                if isinstance(args[0], commands.Context):
                    ctx = args[0]
                # Check if second arg is a commands.Context (for cog methods)
                elif len(args) > 1 and isinstance(args[1], commands.Context):
                    ctx = args[1]
            
            # If we have a context, extract information from it
            if ctx is not None:
                # Add command information
                if hasattr(ctx, "command") and ctx.command is not None:
                    span_attributes["discord.command.name"] = ctx.command.name
                    span_attributes["discord.command.qualified_name"] = ctx.command.qualified_name
                
                # Add guild information
                if hasattr(ctx, "guild") and ctx.guild is not None:
                    span_attributes["discord.guild.id"] = str(ctx.guild.id)
                    span_attributes["discord.guild.name"] = ctx.guild.name
                
                # Add channel information
                if hasattr(ctx, "channel"):
                    span_attributes["discord.channel.id"] = str(ctx.channel.id)
                    span_attributes["discord.channel.name"] = ctx.channel.name
                
                # Add author information
                if hasattr(ctx, "author") and ctx.author is not None:
                    span_attributes["discord.author.id"] = str(ctx.author.id)
                    span_attributes["discord.author.name"] = str(ctx.author)
                
                # Add message information
                if hasattr(ctx, "message") and ctx.message is not None:
                    span_attributes["discord.message.id"] = str(ctx.message.id)
                    if hasattr(ctx.message, "content"):
                        span_attributes["discord.message.content_length"] = len(ctx.message.content)
            
            # Try to extract context from args if it's an event
            elif len(args) > 1:
                # Check if second arg is a Message (for on_message event)
                if isinstance(args[1], discord.Message):
                    message = args[1]
                    span_attributes["discord.message.id"] = str(message.id)
                    if hasattr(message, "content"):
                        span_attributes["discord.message.content_length"] = len(message.content)
                    
                    # Add author information
                    if hasattr(message, "author") and message.author is not None:
                        span_attributes["discord.author.id"] = str(message.author.id)
                        span_attributes["discord.author.name"] = str(message.author)
                    
                    # Add channel information
                    if hasattr(message, "channel"):
                        span_attributes["discord.channel.id"] = str(message.channel.id)
                        span_attributes["discord.channel.name"] = message.channel.name
                    
                    # Add guild information
                    if hasattr(message, "guild") and message.guild is not None:
                        span_attributes["discord.guild.id"] = str(message.guild.id)
                        span_attributes["discord.guild.name"] = message.guild.name
                
                # Check if second arg is a Member (for member events)
                elif isinstance(args[1], discord.Member):
                    member = args[1]
                    span_attributes["discord.member.id"] = str(member.id)
                    span_attributes["discord.member.name"] = str(member)
                    
                    # Add guild information
                    if hasattr(member, "guild") and member.guild is not None:
                        span_attributes["discord.guild.id"] = str(member.guild.id)
                        span_attributes["discord.guild.name"] = member.guild.name
                
                # Check if second arg is a Guild (for guild events)
                elif isinstance(args[1], discord.Guild):
                    guild = args[1]
                    span_attributes["discord.guild.id"] = str(guild.id)
                    span_attributes["discord.guild.name"] = guild.name
            
            # Create a span for the function
            with tracer.start_as_current_span(
                span_name,
                kind=kind,
                attributes=span_attributes,
            ) as span:
                try:
                    # Check if the function is a coroutine function
                    if asyncio.iscoroutinefunction(func):
                        # For async functions, we need to create and run a task
                        async def run_async():
                            result = await func(*args, **kwargs)
                            span.set_status(Status(StatusCode.OK))
                            return result
                        
                        # We can't use asyncio.run here because it creates a new event loop
                        # Instead, we'll just call the function and return the coroutine
                        # The caller is responsible for awaiting it
                        return run_async()
                    else:
                        # For sync functions, just call it directly
                        result = func(*args, **kwargs)
                        span.set_status(Status(StatusCode.OK))
                        return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
        
        return wrapper
    
    # Handle case where decorator is used without parentheses
    if callable(name):
        func, name = name, None
        return decorator(func)
    
    return decorator


def trace_command(
    name: Optional[str] = None,
    attributes: Optional[Dict[str, str]] = None,
) -> Callable:
    """
    Decorator specifically for tracing discord.py commands.
    
    This is a convenience wrapper around the `trace` decorator that sets the
    span kind to SpanKind.CONSUMER, which is appropriate for commands.
    
    Args:
        name: Optional name for the span. If not provided, the function name will be used.
        attributes: Optional attributes to add to the span.
    
    Returns:
        A decorator function that wraps the original function with tracing.
    
    Example:
        ```python
        @bot.command()
        @trace_command(attributes={"custom.attribute": "value"})
        async def my_command(ctx):
            await ctx.send("Hello, world!")
        ```
    """
    return trace(name=name, attributes=attributes, kind=SpanKind.CONSUMER)


def trace_event(
    name: Optional[str] = None,
    attributes: Optional[Dict[str, str]] = None,
) -> Callable:
    """
    Decorator specifically for tracing discord.py event handlers.
    
    This is a convenience wrapper around the `trace` decorator that sets the
    span kind to SpanKind.CONSUMER, which is appropriate for events.
    
    Args:
        name: Optional name for the span. If not provided, the function name will be used.
        attributes: Optional attributes to add to the span.
    
    Returns:
        A decorator function that wraps the original function with tracing.
    
    Example:
        ```python
        @bot.event
        @trace_event(attributes={"custom.attribute": "value"})
        async def on_message(message):
            if message.author == bot.user:
                return
            await message.channel.send("Hello!")
        ```
    """
    return trace(name=name, attributes=attributes, kind=SpanKind.CONSUMER)
