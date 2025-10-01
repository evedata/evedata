import shutil
from typing import TYPE_CHECKING, Annotated

import typer
from typer import Typer

from evedata_platform_extractors._utils._sources import filter_resources

if TYPE_CHECKING:
    from evedata_platform_admin_core import AdminState

cmd = Typer()


@cmd.command(name="hde")
def hde_cmd(
    *,
    ctx: typer.Context,
    version: Annotated[str | None, typer.Option(help="HDE version number.")] = None,
    include: Annotated[
        str | None, typer.Option(help="Comma-separated list of resources to include.")
    ] = None,
    exclude: Annotated[
        str | None,
        typer.Option(help="Comma-separated list of resources to exclude."),
    ] = None,
) -> None:
    """Extract raw data from the HDE."""
    from evedata_platform_extractors._dlt._naming import (  # noqa: PLC0415
        hde as hde_naming_convention,
    )
    from evedata_platform_extractors._dlt._pipelines import (  # noqa: PLC0415
        static_data_pipeline,
    )
    from evedata_platform_extractors._dlt._sources import hde  # noqa: PLC0415
    from evedata_platform_sources._hde import (  # noqa: PLC0415
        archive_current_hde_version,
        current_archived_hde_version,
        stage_archived_hde,
    )

    state: AdminState = ctx.obj
    config = state.config

    version = version or current_archived_hde_version(config)
    if not version:
        version = archive_current_hde_version(config)
    hde_dir = stage_archived_hde(config, version=version)

    source = filter_resources(
        hde(hde_dir, version),
        include=include.split(",") if include else None,
        exclude=exclude.split(",") if exclude else None,
    )

    static_data_pipeline(
        "hde",
        "hde_raw",
        config.catalog_credentials(),
        naming_convention_module=hde_naming_convention,
    ).run(source, loader_file_format="parquet")

    shutil.rmtree(hde_dir, ignore_errors=True)
