"""
OpenTelemetry instrumentation for discord.py
"""

from opentelemetry_instrumentation_discordpy.version import __version__
from opentelemetry_instrumentation_discordpy.instrumentation import DiscordPyInstrumentor

__all__ = ["DiscordPyInstrumentor", "__version__"]
