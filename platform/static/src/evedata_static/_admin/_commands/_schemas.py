from rich.console import Console
from typer import Typer

cmd = Typer(name="schemas")
console = Console()


@cmd.callback()
def callback() -> None:
    """Manage reference data schemas."""


@cmd.command(name="list")
def list_cmd() -> None:
    """List reference data schemas."""
