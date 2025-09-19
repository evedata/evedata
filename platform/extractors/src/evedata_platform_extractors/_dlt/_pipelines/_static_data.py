from typing import TYPE_CHECKING

import dlt
from dlt.common.normalizers.naming import snake_case

if TYPE_CHECKING:
    from types import ModuleType

    from dlt.pipeline.pipeline import Pipeline
    from dlt.pipeline.progress import TCollectorArg
    from evedata_platform_core import Configuration


def static_data_pipeline(
    pipeline_name: str,
    dataset_name: str,
    *,
    config: "Configuration",
    naming_convention_module: "ModuleType | None" = None,
    progress: "TCollectorArg | None" = None,
) -> "Pipeline":
    """Build a DLT pipeline for all static data."""
    naming_convention_module = naming_convention_module or snake_case
    progress = progress or "alive_progress"

    destination = dlt.destinations.duckdb(str(config.duckdb_path))

    return dlt.pipeline(
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
        destination=destination,
        progress=progress,
    )
