from typing import TYPE_CHECKING

import dlt

from evedata_platform_extract._dlt._naming import static as naming_convention_module

if TYPE_CHECKING:
    from dlt.destinations.impl.ducklake.configuration import DuckLakeCredentials
    from dlt.pipeline.pipeline import Pipeline
    from dlt.pipeline.progress import TCollectorArg


def static_data_pipeline(
    pipeline_name: str,
    dataset_name: str,
    credentials: "DuckLakeCredentials",
    *,
    progress: "TCollectorArg | None" = None,
) -> "Pipeline":
    """Build a DLT pipeline for all static data."""
    progress = progress or "alive_progress"

    destination = dlt.destinations.ducklake(
        credentials=credentials,
        loader_parallelism_strategy="parallel",
        naming_convention=naming_convention_module,
    )

    return dlt.pipeline(
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
        destination=destination,
        progress=progress,
    )
