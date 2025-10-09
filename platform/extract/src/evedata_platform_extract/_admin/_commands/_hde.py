import shutil
from typing import TYPE_CHECKING, Annotated

import typer
from typer import Typer

from evedata_platform_extract._utils._sources import filter_resources

if TYPE_CHECKING:
    from evedata_platform_admin_core import AdminState

cmd = Typer()


@cmd.command(name="hde")
def hde_cmd(
    *,
    ctx: typer.Context,
    version: Annotated[int | None, typer.Option(help="HDE version number.")] = None,
    include: Annotated[
        str | None, typer.Option(help="Comma-separated list of resources to include.")
    ] = None,
    exclude: Annotated[
        str | None,
        typer.Option(help="Comma-separated list of resources to exclude."),
    ] = None,
) -> None:
    """Extract raw data from the HDE."""
    from evedata_platform_extract._dlt._pipelines import (
        static_data_pipeline,
    )
    from evedata_platform_extract._dlt._sources import hde
    from evedata_platform_sources._hde import (
        archive_exists,
        create_archive,
        latest_hde_version,
        stage_archive,
    )

    state: AdminState = ctx.obj
    stdout = state.out
    config = state.config
    r2 = config.r2
    bucket = config.sources_bucket

    latest_version = latest_hde_version()
    version = version or latest_version
    if not archive_exists(version, bucket=bucket, r2=r2) and version == latest_version:
        create_archive(bucket=bucket, r2=r2)

    hde_dir = stage_archive(
        config.hde_staging_dir, version=version, bucket=bucket, r2=r2, force=True
    )
    stdout.print("Staged archive in:", hde_dir)

    source = filter_resources(
        hde(hde_dir, version),
        include=include.split(",") if include else None,
        exclude=exclude.split(",") if exclude else None,
    )

    static_data_pipeline("raw_hde", "raw_hde", config.catalog_credentials()).run(
        source, loader_file_format="parquet"
    )

    shutil.rmtree(hde_dir, ignore_errors=True)
