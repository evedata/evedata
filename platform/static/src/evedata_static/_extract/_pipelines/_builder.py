import os
from typing import TYPE_CHECKING

import dlt
from dlt.common.normalizers.naming import snake_case

from evedata_static._constants import SUPPORTED_DESTINATIONS
from evedata_static._exceptions import UnsupportedDestinationError

if TYPE_CHECKING:
    from types import ModuleType

    from dlt.pipeline.pipeline import Pipeline
    from dlt.pipeline.progress import TCollectorArg
    from evedata_core import Configuration


def build_pipeline(  # noqa: PLR0913
    pipeline_name: str,
    dataset_name: str,
    *,
    config: "Configuration",
    destination_name: str | None = None,
    naming_convention_module: "ModuleType | None" = None,
    progress: "TCollectorArg | None" = None,
) -> "Pipeline":
    """Build a DLT pipeline for all static data."""
    data_path = config.data_path
    destination_name = destination_name or "postgres"
    naming_convention_module = naming_convention_module or snake_case
    progress = progress or "alive_progress"

    dlt_dir = data_path / "dlt"
    dlt_dir.mkdir(parents=True, exist_ok=True)
    dlt_data_dir = dlt_dir / "data"
    dlt_pipelines_dir = dlt_dir / "pipelines"

    dlt.config["data_dir"] = str(dlt_data_dir)
    dlt.config["pipelines_dir"] = str(dlt_pipelines_dir)
    dlt.config["extract.workers"] = (os.cpu_count() or 4) * 2

    match destination_name:
        case "duckdb":
            destination = dlt.destinations.duckdb(
                str(config.duckdb_path), naming_convention=naming_convention_module
            )
        case "postgres":
            postgres_host = config.postgres_host
            postgres_port = config.postgres_port
            postgres_user = config.postgres_user
            postgres_password = config.postgres_password
            postgres_db = config.postgres_db
            destination = dlt.destinations.postgres(
                f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}",
                naming_convention=naming_convention_module,
            )
        case _:
            raise UnsupportedDestinationError(
                destination_name, supported=SUPPORTED_DESTINATIONS
            )

    return dlt.pipeline(
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
        destination=destination,
        progress=progress,
    )
