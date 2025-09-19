from typer import Typer

cli = Typer(name="transformations")


@cli.callback()
def callback() -> None:
    """Manage data transformations."""
