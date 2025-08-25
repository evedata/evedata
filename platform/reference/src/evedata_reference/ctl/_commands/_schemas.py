from typer import Typer

cmd = Typer(name="evedata-reference-schemas")


@cmd.callback()
def callback() -> None:
    """Manage reference data schemas."""


@cmd.command(name="drop")
def drop_cmd() -> None:
    """Drop reference data schemas."""


@cmd.command(name="list")
def list_cmd() -> None:
    """List reference data schemas."""
