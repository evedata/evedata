from typer import Typer

cli = Typer(name="transform")


@cli.callback()
def callback() -> None:
    """Manage data transform."""
