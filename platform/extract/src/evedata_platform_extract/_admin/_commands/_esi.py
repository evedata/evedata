from datetime import UTC, datetime
from typing import TYPE_CHECKING

import typer
from typer import Typer

if TYPE_CHECKING:
    from evedata_platform_admin_core import AdminState

cmd = Typer(name="esi", help="Extract raw data from ESI.")


@cmd.command(name="public-market-orders")
def public_market_orders_cmd(
    *,
    ctx: typer.Context,
) -> None:
    """Extract public market orders and 5-minute aggregations."""
    import shutil

    import dlt
    import uvloop
    from dlt.sources.filesystem import filesystem, read_parquet

    from evedata_platform_extract._esi._public_market_orders import (
        extract_public_market_orders,
    )

    state: AdminState = ctx.obj
    config = state.config
    out = state.out

    async def main():
        timestamp = datetime.now(UTC)
        timestamp_str = timestamp.strftime("%Y%m%d%H%M%S")
        tmp_dir = config.cache_dir / "public_market_orders" / timestamp_str
        tmp_dir.mkdir(parents=True, exist_ok=True)

        await extract_public_market_orders(output_dir=str(tmp_dir))

        indicators_filename = tmp_dir / f"market_indicators_5m_{timestamp_str}.parquet"
        orders_filename = tmp_dir / f"market_orders_{timestamp_str}.parquet"
        depth_filename = tmp_dir / f"market_order_depth_{timestamp_str}.parquet"

        destination = dlt.destinations.ducklake(
            credentials=config.catalog_credentials(),
            loader_parallelism_strategy="parallel",
        )

        orders_source = (
            filesystem(bucket_url=f"file:/{orders_filename}", file_glob="")
            | read_parquet()
        )
        orders_source = orders_source.with_name("public_market_orders")
        orders_source = orders_source.apply_hints(write_disposition="append")

        orders_agg_source = (
            filesystem(bucket_url=f"file:/{indicators_filename}", file_glob="")
            | read_parquet()
        )
        orders_agg_source = orders_agg_source.with_name("public_market_orders_agg_5m")
        orders_agg_source = orders_agg_source.apply_hints(write_disposition="append")

        order_depth_source = (
            filesystem(bucket_url=f"file:/{depth_filename}", file_glob="")
            | read_parquet()
        )
        order_depth_source = order_depth_source.with_name("public_market_order_depth")
        order_depth_source = order_depth_source.apply_hints(write_disposition="append")

        pipeline = dlt.pipeline(
            pipeline_name="raw_esi_public_market_orders",
            dataset_name="raw_esi",
            destination=destination,
            progress="alive_progress",
        )
        load_info = pipeline.run(
            [orders_source, orders_agg_source, order_depth_source],
            loader_file_format="parquet",
        )

        out.print(load_info)

        shutil.rmtree(tmp_dir)

    uvloop.run(main())
