from typing import TYPE_CHECKING

import typer
from typer import Typer

if TYPE_CHECKING:
    from evedata_platform_admin_core import AdminState

cmd = Typer()


@cmd.command(name="public-market-orders")
def public_market_orders_cmd(*, ctx: typer.Context) -> None:
    """Extract public market orders from ESI."""
    from evedata_platform_extractors._dlt._pipelines import (  # noqa: PLC0415
        public_market_orders_pipeline,
    )
    from evedata_platform_extractors._dlt._sources import (  # noqa: PLC0415
        esi_public_market_orders,
    )

    state: AdminState = ctx.obj
    config = state.config
    source = esi_public_market_orders(config.http_cache_dir)

    public_market_orders_pipeline(config=config).run(
        source, loader_file_format="parquet"
    )
