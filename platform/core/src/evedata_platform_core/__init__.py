"""Provides core functionality for the EVEData platform."""

from ._config import Configuration, get_config

__all__ = ["Configuration", "get_config"]

if __name__ == "__main__":
    from rich.console import Console

    config = get_config()
    console = Console()
    console.print(config.model_dump())
