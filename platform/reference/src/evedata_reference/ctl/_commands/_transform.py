from typer import Typer

cmd = Typer()


@cmd.command(name="transform")
def transform_cmd() -> None:
    """Transform reference data from raw datasets."""
