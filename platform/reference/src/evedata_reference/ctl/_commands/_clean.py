from typing import Annotated

import typer
from typer import Typer

cmd = Typer()


@cmd.command(name="clean")
def clean_cmd(
    schemas: Annotated[
        str | None, typer.Option(help="Schemas to drop, comma-separated.")
    ] = None,
) -> None:
    """Clean reference data."""
    import duckdb  # noqa: PLC0415

    if not schemas:
        schema_names = ["esi_raw", "hde_raw", "sde_raw", "staging"]
    else:
        schema_names = [s.strip() for s in schemas.split(",") if s.strip()]

    with duckdb.connect() as conn:
        for schema in schema_names:
            conn.sql(f"DROP SCHEMA {schema} CASCADE").execute()
