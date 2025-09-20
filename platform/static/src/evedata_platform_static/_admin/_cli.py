from typer import Typer

from ._commands import (
    export_cmd,
    publish_cmd,
)

cli = Typer(name="static")
cli.add_typer(export_cmd)
cli.add_typer(publish_cmd)


@cli.callback()
def callback() -> None:
    """Manage static data."""
