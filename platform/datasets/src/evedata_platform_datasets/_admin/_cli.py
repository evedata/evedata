from typer import Typer

cli = Typer(name="evedata-platform-datasets")


@cli.callback()
def callback() -> None:
    """Manage datasets."""
