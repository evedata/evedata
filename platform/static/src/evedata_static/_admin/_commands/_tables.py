from typing import Annotated

import typer
from rich.console import Console
from typer import Typer

cmd = Typer(name="tables")
console = Console()


@cmd.callback()
def callback() -> None:
    """Manage reference data tables."""


@cmd.command(name="list")
def list_cmd(schema: Annotated[str, typer.Argument(help="Schema to query.")]) -> None:
    """List reference data tables."""
