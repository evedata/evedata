from typing import Annotated

import typer
from typer import Typer

cmd = Typer()


@cmd.command(name="clean")
def clean_cmd(
    schemas: Annotated[
        str | None, typer.Option(help="Schemas to drop, comma-separated.")
    ] = None,
) -> None:
    """Clean reference data."""
