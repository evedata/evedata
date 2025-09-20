from typer import Typer

from ._commands import sde_cmd

cli = Typer(name="evedata-platform-sources")
cli.add_typer(sde_cmd)


@cli.callback()
def callback() -> None:
    """Manage raw data sources."""
