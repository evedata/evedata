from typing import TYPE_CHECKING

import dlt

if TYPE_CHECKING:
    from dlt.pipeline.pipeline import Pipeline
    from dlt.pipeline.progress import TCollectorArg
    from evedata_platform_core import Configuration


def public_market_orders_pipeline(
    *,
    config: "Configuration",
    progress: "TCollectorArg | None" = None,
) -> "Pipeline":
    """Build a DLT pipeline for public market orders."""
    progress = progress or "alive_progress"

    destination = dlt.destinations.duckdb(str(config.duckdb_path))

    return dlt.pipeline(
        pipeline_name="esi_public_market_orders",
        dataset_name="esi_public_market_orders_raw",
        destination=destination,
        progress=progress,
    )
