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
    version: Annotated[int | None, typer.Option(help="SDE version to extract.")] = None,
    include: Annotated[
        str | None, typer.Option(help="Comma-separated list of resources to include.")
    ] = None,
    exclude: Annotated[
        str | None,
        typer.Option(help="Comma-separated list of resources to exclude."),
    ] = None,
) -> None:
    """Extract raw data from the SDE."""
    from evedata_platform_extract._dlt._pipelines import (
        static_data_pipeline,
    )
    from evedata_platform_extract._dlt._sources._sde import sde
    from evedata_platform_extract._utils._sources import (
        filter_resources,
    )
    from evedata_platform_sources._sde import (
        archive_exists,
        create_archive,
        latest_sde_version,
        stage_archive,
    )

    state: AdminState = ctx.obj
    stdout = state.out
    config = state.config
    r2 = config.r2
    bucket = config.sources_bucket

    version = version or latest_sde_version()
    if not archive_exists(version, bucket=bucket, r2=r2):
        create_archive(version, bucket=bucket, r2=r2)

    sde_dir = stage_archive(
        config.sde_staging_dir, version=version, bucket=bucket, r2=r2, force=True
    )
    stdout.print("Staged archive in:", sde_dir)

    source = filter_resources(
        sde(sde_dir, version),
        include=include.split(",") if include else None,
        exclude=exclude.split(",") if exclude else None,
    )

    static_data_pipeline("raw_sde", "raw_sde", config.catalog_credentials()).run(
        source, loader_file_format="parquet"
    )

    shutil.rmtree(sde_dir.parent, ignore_errors=True)
