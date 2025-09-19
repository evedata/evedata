from typing import TYPE_CHECKING

import typer
from typer import Typer

from ._commands import (
    hde_cmd,
    public_market_orders_cmd,
    sde_cmd,
)

if TYPE_CHECKING:
    from evedata_platform_admin_core import AdminState

cli = Typer(name="extract")
cli.add_typer(hde_cmd)
cli.add_typer(public_market_orders_cmd)
cli.add_typer(sde_cmd)


@cli.callback()
def callback(ctx: typer.Context) -> None:
    """Extract raw data from EVE Online sources."""
    import os  # noqa: PLC0415

    import dlt  # noqa: PLC0415

    state: AdminState = ctx.obj
    config = state.config
    data_path = config.data_path

    dlt_dir = data_path / "dlt"
    dlt_dir.mkdir(parents=True, exist_ok=True)
    dlt_data_dir = dlt_dir / "data"
    dlt_pipelines_dir = dlt_dir / "pipelines"

    dlt.config["data_dir"] = str(dlt_data_dir)
    dlt.config["pipelines_dir"] = str(dlt_pipelines_dir)
    dlt.config["extract.max_parallel_items"] = 100
    dlt.config["extract.workers"] = (os.cpu_count() or 4) * 2
