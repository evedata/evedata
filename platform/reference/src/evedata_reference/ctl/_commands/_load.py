from typer import Typer

cmd = Typer()


@cmd.command(name="load")
def load_cmd() -> None:
    """Load reference datasets."""
