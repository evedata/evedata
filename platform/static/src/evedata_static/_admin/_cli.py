from typer import Typer

from ._commands import (
    clean_cmd,
    download_cmd,
    export_cmd,
    extract_cmd,
    publish_cmd,
    schemas_cmd,
    tables_cmd,
    transform_cmd,
)

cli = Typer(name="static")
cli.add_typer(clean_cmd)
cli.add_typer(download_cmd)
cli.add_typer(export_cmd)
cli.add_typer(extract_cmd)
cli.add_typer(publish_cmd)
cli.add_typer(schemas_cmd)
cli.add_typer(tables_cmd)
cli.add_typer(transform_cmd)


@cli.callback()
def callback() -> None:
    """Manage static data."""
