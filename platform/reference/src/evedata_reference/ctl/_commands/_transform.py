from typer import Typer

cmd = Typer(name="evedata-reference-transform")


@cmd.command(name="transform")
def transform_cmd() -> None:
    """Transform reference data from raw datasets."""
