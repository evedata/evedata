import shutil
from typing import TYPE_CHECKING, Annotated

import typer
from typer import Typer

if TYPE_CHECKING:
    from evedata_platform_admin_core import AdminState

cmd = Typer()


@cmd.command(name="sde")
def sde_cmd(
    *,
    ctx: typer.Context,
    version: Annotated[
        str | None, typer.Option(help="SDE version to extract in YYYYMMDD format.")
    ] = None,
    include: Annotated[
        str | None, typer.Option(help="Comma-separated list of resources to include.")
    ] = None,
    exclude: Annotated[
        str | None,
        typer.Option(help="Comma-separated list of resources to exclude."),
    ] = None,
) -> None:
    """Extract raw data from the SDE."""
    from evedata_platform_extract._dlt._pipelines import (  # noqa: PLC0415
        static_data_pipeline,
    )
    from evedata_platform_extract._dlt._sources import sde  # noqa: PLC0415
    from evedata_platform_extract._utils._sources import (  # noqa: PLC0415
        filter_resources,
    )
    from evedata_platform_sources._sde import (  # noqa: PLC0415
        archive_current_sde_version,
        current_archived_sde_version,
        stage_archived_sde,
    )

    state: AdminState = ctx.obj
    config = state.config

    version = version or current_archived_sde_version(config)
    if not version:
        version = archive_current_sde_version(config)
    sde_dir = stage_archived_sde(config, version=version)

    source = filter_resources(
        sde(sde_dir, version),
        include=include.split(",") if include else None,
        exclude=exclude.split(",") if exclude else None,
    )

    static_data_pipeline("sde", "sde_raw", config.catalog_credentials()).run(
        source, loader_file_format="parquet"
    )

    shutil.rmtree(sde_dir, ignore_errors=True)
