from typer import Typer

cli = Typer(name="evedata-datasets")


@cli.callback()
def callback() -> None:
    """Manage datasets."""
