from rich.console import Console
from typer import Typer

from evedata_reference._paths import default_duckdb_path

cmd = Typer(name="schemas")
console = Console()


@cmd.callback()
def callback() -> None:
    """Manage reference data schemas."""


@cmd.command(name="list")
def list_cmd() -> None:
    """List reference data schemas."""
    import duckdb  # noqa: PLC0415

    with duckdb.connect(default_duckdb_path()) as conn:
        res = conn.sql(
            "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name"
        ).fetchall()
        for row in res:
            console.print(row[0])
