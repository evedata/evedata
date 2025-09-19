"""Plugin for evedata-ctl for static data management."""

from ._app import app
from ._cli import cli

__all__ = ["app", "cli"]
