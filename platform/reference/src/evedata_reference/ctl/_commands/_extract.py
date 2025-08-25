from typer import Typer

cmd = Typer(name="evedata-reference-extract")


@cmd.command(name="extract")
def extract_cmd() -> None:
    """Extract reference data from raw sources."""
