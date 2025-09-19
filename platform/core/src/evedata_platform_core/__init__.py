"""Provides core functionality for the EVEData platform."""

from ._config import Configuration, get_config
from ._constants import EVEDATA_USER_AGENT

__all__ = ["EVEDATA_USER_AGENT", "Configuration", "get_config"]
