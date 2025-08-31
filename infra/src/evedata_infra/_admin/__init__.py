"""Plugin for evedata-ctl for infrastructure tasks."""

from ._app import app
from ._cli import cli

__all__ = ["app", "cli"]
