from typer import Typer

cmd = Typer(name="evedata-reference-tables")


@cmd.callback()
def callback() -> None:
    """Manage reference data tables."""


@cmd.command(name="drop")
def drop_cmd() -> None:
    """Drop reference data tables."""


@cmd.command(name="list")
def list_cmd() -> None:
    """List reference data tables."""
