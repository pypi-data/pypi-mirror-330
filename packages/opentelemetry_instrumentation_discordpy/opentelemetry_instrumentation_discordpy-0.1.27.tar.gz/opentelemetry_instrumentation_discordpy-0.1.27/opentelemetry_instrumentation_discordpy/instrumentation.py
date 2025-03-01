"""
OpenTelemetry instrumentation for discord.py
"""

import logging
from typing import Collection, Dict, Optional, Sequence

import discord
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import TracerProvider, get_tracer

from opentelemetry_instrumentation_discordpy.metrics import setup_metrics, wrap_metrics, unwrap_metrics
from opentelemetry_instrumentation_discordpy.wrappers import (
    commands,
    event_listeners,
    http,
    message_operations,
    voice,
)

logger = logging.getLogger(__name__)


class DiscordPyInstrumentor(BaseInstrumentor):
    """
    An instrumentor for discord.py
    
    This class provides instrumentation for discord.py, enabling automatic
    tracing of events, commands, message operations, HTTP requests, and voice
    operations.
    """
    
    def __init__(self):
        super().__init__()
        self._tracer = None
        self._instrumented = False
        self._wrapped_components = set()
        self._custom_events = set()
    
    def add_custom_event(self, event_name: str) -> "DiscordPyInstrumentor":
        """
        Register a custom event to be instrumented.
        
        Args:
            event_name: The name of the event to register (e.g., "on_rabbitmq_message")
            
        Returns:
            The instrumentor instance for chaining
        """
        event_listeners.register_custom_event(event_name)
        self._custom_events.add(event_name)
        return self
    
    def remove_custom_event(self, event_name: str) -> "DiscordPyInstrumentor":
        """
        Unregister a custom event.
        
        Args:
            event_name: The name of the event to unregister
            
        Returns:
            The instrumentor instance for chaining
        """
        event_listeners.unregister_custom_event(event_name)
        if event_name in self._custom_events:
            self._custom_events.remove(event_name)
        return self
    
    def instrumentation_dependencies(self) -> Collection[str]:
        """
        Returns a collection of instrumentations that this instrumentor depends on.
        """
        return []
    
    def _instrument(self, **kwargs):
        """
        Instruments discord.py.
        
        Args:
            **kwargs: Optional keyword arguments.
                tracer_provider: The tracer provider to use. If not provided,
                    the global tracer provider is used.
                collect_metrics: Whether to collect metrics. Defaults to True.
                instrument_event_listeners: Whether to instrument event listeners.
                    Defaults to True.
                instrument_message_operations: Whether to instrument message operations.
                    Defaults to True.
                instrument_commands: Whether to instrument commands.
                    Defaults to True.
                instrument_http: Whether to instrument HTTP requests.
                    Defaults to True.
                instrument_voice: Whether to instrument voice operations.
                    Defaults to True.
        """
        if self._instrumented:
            logger.warning("Discord.py is already instrumented")
            return
        
        # Get configuration options
        tracer_provider = kwargs.get("tracer_provider")
        collect_metrics = kwargs.get("collect_metrics", True)
        instrument_event_listeners = kwargs.get("instrument_event_listeners", True)
        instrument_message_operations = kwargs.get("instrument_message_operations", True)
        instrument_commands = kwargs.get("instrument_commands", True)
        instrument_http = kwargs.get("instrument_http", True)
        instrument_voice = kwargs.get("instrument_voice", True)
        
        # Set up the tracer
        self._tracer = get_tracer(
            "discord.py",
            tracer_provider=tracer_provider,
        )
        
        # Instrument components based on configuration
        if instrument_event_listeners:
            event_listeners.wrap_event_listeners()
            self._wrapped_components.add("event_listeners")
        
        if instrument_message_operations:
            message_operations.wrap_message_operations()
            self._wrapped_components.add("message_operations")
        
        if instrument_commands:
            commands.wrap_commands()
            self._wrapped_components.add("commands")
        
        if instrument_http:
            http.wrap_http()
            self._wrapped_components.add("http")
        
        if instrument_voice:
            voice.wrap_voice()
            self._wrapped_components.add("voice")
        
        # Set up metrics if enabled
        if collect_metrics:
            setup_metrics()
            wrap_metrics()
            self._wrapped_components.add("metrics")
        
        self._instrumented = True
        logger.debug("Discord.py instrumentation complete")
    
    def _uninstrument(self, **kwargs):
        """
        Uninstruments discord.py.
        """
        if not self._instrumented:
            logger.warning("Discord.py is not instrumented")
            return
        
        # Uninstrument components
        if "event_listeners" in self._wrapped_components:
            event_listeners.unwrap_event_listeners()
        
        if "message_operations" in self._wrapped_components:
            message_operations.unwrap_message_operations()
        
        if "commands" in self._wrapped_components:
            commands.unwrap_commands()
        
        if "http" in self._wrapped_components:
            http.unwrap_http()
        
        if "voice" in self._wrapped_components:
            voice.unwrap_voice()
        
        if "metrics" in self._wrapped_components:
            unwrap_metrics()
        
        self._wrapped_components.clear()
        self._instrumented = False
        logger.debug("Discord.py instrumentation removed")
