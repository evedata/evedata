from typer import Typer

cmd = Typer(name="evedata-reference-load")


@cmd.command(name="load")
def load_cmd() -> None:
    """Load reference datasets."""
