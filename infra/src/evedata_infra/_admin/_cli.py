from typer import Typer

cli = Typer(name="evedata-infra")


@cli.callback()
def callback():
    """Manage infrastructure."""


@cli.command(name="status")
def status_cmd():
    """Check infrastructure status."""
