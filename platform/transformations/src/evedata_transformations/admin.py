"""Provides plugins for EVEData Admin."""

from ._admin import app as endpoints, cli as commands

__all__ = [
    "commands",
    "endpoints",
]
