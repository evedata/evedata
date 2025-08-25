from typing import Annotated

import typer
from rich.console import Console
from typer import Typer

from evedata_reference._paths import default_duckdb_path

cmd = Typer(name="tables")
console = Console()


@cmd.callback()
def callback() -> None:
    """Manage reference data tables."""


@cmd.command(name="list")
def list_cmd(schema: Annotated[str, typer.Argument(help="Schema to query.")]) -> None:
    """List reference data tables."""
    if not schema:
        typer.echo("Schema is required.")
        raise typer.Exit(code=2)

    import duckdb  # noqa: PLC0415

    with duckdb.connect(default_duckdb_path()) as conn:
        res = conn.sql(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = ?
            ORDER BY table_name
            """,
            params=[schema],
        ).fetchall()
        for row in res:
            console.print(row[0])
