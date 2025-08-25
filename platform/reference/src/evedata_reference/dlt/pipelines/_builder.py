import os
from pathlib import Path
from typing import TYPE_CHECKING

import dlt
from dlt.common.normalizers.naming import snake_case

from evedata_reference._constants import SUPPORTED_DESTINATIONS
from evedata_reference._exceptions import UnsupportedDestinationError

if TYPE_CHECKING:
    from types import ModuleType

    from dlt.pipeline.pipeline import Pipeline
    from dlt.pipeline.progress import TCollectorArg


def build_pipeline(  # noqa: PLR0913
    pipeline_name: str,
    dataset_name: str,
    *,
    destination_name: str | None = None,
    destination_path: Path | None = None,
    naming_convention_module: "ModuleType | None" = None,
    import_schema_path: str | None = None,
    export_schema_path: str | None = None,
    data_dir: Path | None = None,
    pipelines_dir: Path | None = None,
    progress: "TCollectorArg | None" = None,
) -> "Pipeline":
    """Build a DLT pipeline for all static data."""
    destination_name = destination_name or "duckdb"
    naming_convention_module = naming_convention_module or snake_case
    import_schema_path = import_schema_path or str(
        Path.cwd() / "data" / "schemas" / "import" / pipeline_name / destination_name
    )
    export_schema_path = export_schema_path or str(
        Path.cwd() / "data" / "schemas" / "export" / pipeline_name / destination_name
    )
    progress = progress or "alive_progress"

    destination_path = destination_path or (Path.cwd() / "data" / "evedata_reference.duckdb")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    data_dir = data_dir or (Path.cwd() / "data" / "dlt" / "data")
    data_dir.mkdir(parents=True, exist_ok=True)
    pipelines_dir = pipelines_dir or (Path.cwd() / "data" / "dlt" / "pipelines")
    pipelines_dir.mkdir(parents=True, exist_ok=True)

    dlt.config["data_dir"] = str(data_dir)
    dlt.config["pipelines_dir"] = str(pipelines_dir)
    dlt.config["extract.workers"] = (os.cpu_count() or 4) * 2

    match destination_name:
        case "duckdb":
            destination = dlt.destinations.duckdb(str(destination_path), naming_convention=naming_convention_module)
        case _:
            raise UnsupportedDestinationError(destination_name, supported=SUPPORTED_DESTINATIONS)

    return dlt.pipeline(
        pipeline_name=pipeline_name,
        dataset_name=dataset_name,
        destination=destination,
        import_schema_path=import_schema_path,
        export_schema_path=export_schema_path,
        progress=progress,
    )
