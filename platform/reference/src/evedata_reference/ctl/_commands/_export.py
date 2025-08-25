from typer import Typer

cmd = Typer(name="evedata-reference-export")


@cmd.command(name="extract")
def export_cmd() -> None:
    """Export reference datasets."""
