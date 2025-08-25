from typer import Typer

cmd = Typer()


@cmd.command(name="export")
def export_cmd() -> None:
    """Export reference datasets."""
