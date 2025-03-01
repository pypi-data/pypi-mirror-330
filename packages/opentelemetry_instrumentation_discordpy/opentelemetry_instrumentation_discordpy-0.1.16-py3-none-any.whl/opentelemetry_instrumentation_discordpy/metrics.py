"""
Metrics collection for discord.py
"""

import functools
import logging
from typing import Any, Callable, Dict, Optional, cast

import discord
from discord.client import Client
from discord.ext import commands
from opentelemetry import metrics
from opentelemetry.metrics import Counter, Histogram, UpDownCounter

logger = logging.getLogger(__name__)

# Original methods that we're wrapping
_WRAPPED_METHODS = {}

# Metrics
_METRICS: Dict[str, Any] = {}


def _initialize_metrics() -> None:
    """
    Initialize metrics for discord.py.
    """
    meter = metrics.get_meter("discord.py")
    
    # Message metrics
    _METRICS["messages_received"] = meter.create_counter(
        "discord.messages.received",
        description="Number of messages received",
        unit="1",
    )
    
    _METRICS["messages_sent"] = meter.create_counter(
        "discord.messages.sent",
        description="Number of messages sent",
        unit="1",
    )
    
    _METRICS["messages_edited"] = meter.create_counter(
        "discord.messages.edited",
        description="Number of messages edited",
        unit="1",
    )
    
    _METRICS["messages_deleted"] = meter.create_counter(
        "discord.messages.deleted",
        description="Number of messages deleted",
        unit="1",
    )
    
    # Command metrics
    _METRICS["commands_invoked"] = meter.create_counter(
        "discord.commands.invoked",
        description="Number of commands invoked",
        unit="1",
    )
    
    _METRICS["commands_completed"] = meter.create_counter(
        "discord.commands.completed",
        description="Number of commands completed successfully",
        unit="1",
    )
    
    _METRICS["commands_errors"] = meter.create_counter(
        "discord.commands.errors",
        description="Number of command errors",
        unit="1",
    )
    
    # API metrics
    _METRICS["api_requests"] = meter.create_counter(
        "discord.api.requests",
        description="Number of API requests",
        unit="1",
    )
    
    _METRICS["api_errors"] = meter.create_counter(
        "discord.api.errors",
        description="Number of API errors",
        unit="1",
    )
    
    _METRICS["api_latency"] = meter.create_histogram(
        "discord.api.latency",
        description="API request latency",
        unit="ms",
    )
    
    # Voice metrics
    _METRICS["voice_connections"] = meter.create_up_down_counter(
        "discord.voice.connections",
        description="Number of active voice connections",
        unit="1",
    )
    
    _METRICS["voice_playback_time"] = meter.create_counter(
        "discord.voice.playback_time",
        description="Total voice playback time",
        unit="s",
    )
    
    # Guild metrics
    _METRICS["guilds"] = meter.create_up_down_counter(
        "discord.guilds",
        description="Number of guilds the bot is in",
        unit="1",
    )
    
    # Member metrics
    _METRICS["members"] = meter.create_up_down_counter(
        "discord.members",
        description="Number of members in guilds",
        unit="1",
    )
    
    # Event metrics
    _METRICS["events"] = meter.create_counter(
        "discord.events",
        description="Number of events received",
        unit="1",
    )
    
    # Reaction metrics
    _METRICS["reactions_added"] = meter.create_counter(
        "discord.reactions.added",
        description="Number of reactions added",
        unit="1",
    )
    
    _METRICS["reactions_removed"] = meter.create_counter(
        "discord.reactions.removed",
        description="Number of reactions removed",
        unit="1",
    )


def _wrap_on_ready(original_func: Callable) -> Callable:
    """
    Wrap on_ready to collect guild and member metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_on_ready(*args: Any, **kwargs: Any) -> Any:
        client = args[0]
        
        # Record guild count
        guild_count = len(client.guilds)
        _METRICS["guilds"].add(guild_count)
        
        # Record member count
        member_count = sum(guild.member_count for guild in client.guilds if hasattr(guild, "member_count"))
        _METRICS["members"].add(member_count)
        
        # Record event
        _METRICS["events"].add(1, {"event": "on_ready"})
        
        return await original_func(*args, **kwargs)
    
    return instrumented_on_ready


def _wrap_on_message(original_func: Callable) -> Callable:
    """
    Wrap on_message to collect message metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_on_message(*args: Any, **kwargs: Any) -> Any:
        message = args[1]
        
        # Record message received
        attributes = {
            "guild_id": str(message.guild.id) if hasattr(message, "guild") and message.guild else "dm",
            "channel_id": str(message.channel.id) if hasattr(message, "channel") else "unknown",
            "is_bot": message.author.bot if hasattr(message.author, "bot") else False,
        }
        _METRICS["messages_received"].add(1, attributes)
        
        # Record event
        _METRICS["events"].add(1, {"event": "on_message"})
        
        return await original_func(*args, **kwargs)
    
    return instrumented_on_message


def _wrap_on_guild_join(original_func: Callable) -> Callable:
    """
    Wrap on_guild_join to collect guild metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_on_guild_join(*args: Any, **kwargs: Any) -> Any:
        guild = args[1]
        
        # Increment guild count
        _METRICS["guilds"].add(1)
        
        # Increment member count
        member_count = guild.member_count if hasattr(guild, "member_count") else 0
        _METRICS["members"].add(member_count)
        
        # Record event
        _METRICS["events"].add(1, {"event": "on_guild_join"})
        
        return await original_func(*args, **kwargs)
    
    return instrumented_on_guild_join


def _wrap_on_guild_remove(original_func: Callable) -> Callable:
    """
    Wrap on_guild_remove to collect guild metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_on_guild_remove(*args: Any, **kwargs: Any) -> Any:
        guild = args[1]
        
        # Decrement guild count
        _METRICS["guilds"].add(-1)
        
        # Decrement member count
        member_count = guild.member_count if hasattr(guild, "member_count") else 0
        _METRICS["members"].add(-member_count)
        
        # Record event
        _METRICS["events"].add(1, {"event": "on_guild_remove"})
        
        return await original_func(*args, **kwargs)
    
    return instrumented_on_guild_remove


def _wrap_on_member_join(original_func: Callable) -> Callable:
    """
    Wrap on_member_join to collect member metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_on_member_join(*args: Any, **kwargs: Any) -> Any:
        # Increment member count
        _METRICS["members"].add(1)
        
        # Record event
        _METRICS["events"].add(1, {"event": "on_member_join"})
        
        return await original_func(*args, **kwargs)
    
    return instrumented_on_member_join


def _wrap_on_member_remove(original_func: Callable) -> Callable:
    """
    Wrap on_member_remove to collect member metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_on_member_remove(*args: Any, **kwargs: Any) -> Any:
        # Decrement member count
        _METRICS["members"].add(-1)
        
        # Record event
        _METRICS["events"].add(1, {"event": "on_member_remove"})
        
        return await original_func(*args, **kwargs)
    
    return instrumented_on_member_remove


def _wrap_on_reaction_add(original_func: Callable) -> Callable:
    """
    Wrap on_reaction_add to collect reaction metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_on_reaction_add(*args: Any, **kwargs: Any) -> Any:
        # Record reaction added
        _METRICS["reactions_added"].add(1)
        
        # Record event
        _METRICS["events"].add(1, {"event": "on_reaction_add"})
        
        return await original_func(*args, **kwargs)
    
    return instrumented_on_reaction_add


def _wrap_on_reaction_remove(original_func: Callable) -> Callable:
    """
    Wrap on_reaction_remove to collect reaction metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_on_reaction_remove(*args: Any, **kwargs: Any) -> Any:
        # Record reaction removed
        _METRICS["reactions_removed"].add(1)
        
        # Record event
        _METRICS["events"].add(1, {"event": "on_reaction_remove"})
        
        return await original_func(*args, **kwargs)
    
    return instrumented_on_reaction_remove


def _wrap_send_message(original_func: Callable) -> Callable:
    """
    Wrap TextChannel.send to collect message metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_send(*args: Any, **kwargs: Any) -> Any:
        channel = args[0]
        
        result = await original_func(*args, **kwargs)
        
        # Record message sent
        attributes = {
            "guild_id": str(channel.guild.id) if hasattr(channel, "guild") and channel.guild else "dm",
            "channel_id": str(channel.id) if hasattr(channel, "id") else "unknown",
        }
        _METRICS["messages_sent"].add(1, attributes)
        
        return result
    
    return instrumented_send


def _wrap_edit_message(original_func: Callable) -> Callable:
    """
    Wrap Message.edit to collect message metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_edit(*args: Any, **kwargs: Any) -> Any:
        message = args[0]
        
        result = await original_func(*args, **kwargs)
        
        # Record message edited
        attributes = {
            "guild_id": str(message.guild.id) if hasattr(message, "guild") and message.guild else "dm",
            "channel_id": str(message.channel.id) if hasattr(message, "channel") else "unknown",
        }
        _METRICS["messages_edited"].add(1, attributes)
        
        return result
    
    return instrumented_edit


def _wrap_delete_message(original_func: Callable) -> Callable:
    """
    Wrap Message.delete to collect message metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_delete(*args: Any, **kwargs: Any) -> Any:
        message = args[0]
        
        result = await original_func(*args, **kwargs)
        
        # Record message deleted
        attributes = {
            "guild_id": str(message.guild.id) if hasattr(message, "guild") and message.guild else "dm",
            "channel_id": str(message.channel.id) if hasattr(message, "channel") else "unknown",
        }
        _METRICS["messages_deleted"].add(1, attributes)
        
        return result
    
    return instrumented_delete


def _wrap_command_invoke(original_func: Callable) -> Callable:
    """
    Wrap Command.invoke to collect command metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_invoke(*args: Any, **kwargs: Any) -> Any:
        command = args[0]
        ctx = args[1]
        
        # Record command invoked
        attributes = {
            "command": command.qualified_name,
            "guild_id": str(ctx.guild.id) if hasattr(ctx, "guild") and ctx.guild else "dm",
            "channel_id": str(ctx.channel.id) if hasattr(ctx, "channel") else "unknown",
        }
        _METRICS["commands_invoked"].add(1, attributes)
        
        try:
            result = await original_func(*args, **kwargs)
            
            # Record command completed
            _METRICS["commands_completed"].add(1, attributes)
            
            return result
        except Exception as e:
            # Record command error
            error_attributes = {**attributes, "error_type": e.__class__.__name__}
            _METRICS["commands_errors"].add(1, error_attributes)
            
            raise
    
    return instrumented_invoke


def _wrap_voice_connect(original_func: Callable) -> Callable:
    """
    Wrap VoiceClient.connect to collect voice metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_connect(*args: Any, **kwargs: Any) -> Any:
        voice_client = args[0]
        
        result = await original_func(*args, **kwargs)
        
        # Increment voice connection count
        attributes = {
            "guild_id": str(voice_client.guild.id) if hasattr(voice_client, "guild") and voice_client.guild else "unknown",
            "channel_id": str(voice_client.channel.id) if hasattr(voice_client, "channel") else "unknown",
        }
        _METRICS["voice_connections"].add(1, attributes)
        
        return result
    
    return instrumented_connect


def _wrap_voice_disconnect(original_func: Callable) -> Callable:
    """
    Wrap VoiceClient.disconnect to collect voice metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_disconnect(*args: Any, **kwargs: Any) -> Any:
        voice_client = args[0]
        
        # Decrement voice connection count
        attributes = {
            "guild_id": str(voice_client.guild.id) if hasattr(voice_client, "guild") and voice_client.guild else "unknown",
            "channel_id": str(voice_client.channel.id) if hasattr(voice_client, "channel") else "unknown",
        }
        _METRICS["voice_connections"].add(-1, attributes)
        
        return await original_func(*args, **kwargs)
    
    return instrumented_disconnect


def _wrap_http_request(original_func: Callable) -> Callable:
    """
    Wrap HTTPClient.request to collect API metrics.
    """
    @functools.wraps(original_func)
    async def instrumented_request(*args: Any, **kwargs: Any) -> Any:
        route = args[1]
        
        # Record API request
        attributes = {
            "method": route.method,
            "path": route.path,
        }
        _METRICS["api_requests"].add(1, attributes)
        
        import time
        start_time = time.time()
        
        try:
            result = await original_func(*args, **kwargs)
            
            # Record API latency
            latency_ms = (time.time() - start_time) * 1000
            _METRICS["api_latency"].record(latency_ms, attributes)
            
            return result
        except Exception as e:
            # Record API error
            error_attributes = {**attributes, "error_type": e.__class__.__name__}
            _METRICS["api_errors"].add(1, error_attributes)
            
            raise
    
    return instrumented_request


def setup_metrics() -> None:
    """
    Set up metrics collection for discord.py.
    """
    logger.debug("Setting up metrics collection for discord.py")
    
    # Initialize metrics
    _initialize_metrics()


def wrap_metrics() -> None:
    """
    Wrap discord.py methods to collect metrics.
    """
    logger.debug("Instrumenting discord.py for metrics collection")
    
    # Ensure metrics are initialized
    if not _METRICS:
        setup_metrics()
    
    # Wrap Client event methods
    if hasattr(Client, "dispatch"):
        original_dispatch = Client.dispatch
        
        @functools.wraps(original_dispatch)
        def instrumented_dispatch(self, event, *args, **kwargs):
            # Record event
            _METRICS["events"].add(1, {"event": event})
            
            return original_dispatch(self, event, *args, **kwargs)
        
        Client.dispatch = instrumented_dispatch
    
    # Store original methods for unwrapping later
    _WRAPPED_METHODS["Client.dispatch"] = getattr(Client, "dispatch", None)


def unwrap_metrics() -> None:
    """
    Unwrap discord.py methods, removing metrics collection.
    """
    logger.debug("Removing metrics collection from discord.py")
    
    # Restore original methods
    for method_path, original_method in _WRAPPED_METHODS.items():
        if original_method is not None:
            class_name, method_name = method_path.split(".")
            if class_name == "Client":
                setattr(Client, method_name, original_method)
    
    # Clear wrapped methods
    _WRAPPED_METHODS.clear()
