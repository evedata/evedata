from typer import Typer

from ._commands import hde_cmd, sde_cmd

cli = Typer(name="evedata-platform-sources")
cli.add_typer(hde_cmd)
cli.add_typer(sde_cmd)


@cli.callback()
def callback() -> None:
    """Manage raw data sources."""
