import shutil
from typing import TYPE_CHECKING, Annotated

import duckdb
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
    from evedata_platform_extractors._dlt._pipelines import (  # noqa: PLC0415
        static_data_pipeline,
    )
    from evedata_platform_extractors._dlt._sources import sde  # noqa: PLC0415
    from evedata_platform_extractors._utils._sources import (  # noqa: PLC0415
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

    db_path = config.sde_staging_dir / f"sde-{version}-staging.duckdb"
    db = duckdb.connect(db_path)  # pyright: ignore[reportUnknownMemberType]

    static_data_pipeline("sde", "sde_raw", db).run(source, loader_file_format="parquet")

    db.install_extension("postgres")
    db.execute(f"""
        CREATE SECRET(
            TYPE postgres,
            HOST '{config.ducklake_host}',
            PORT {config.ducklake_port},
            USER '{config.ducklake_user}',
            PASSWORD '{config.ducklake_password}',
            DATABASE '{config.ducklake_database}'
        );
    """)
    db.install_extension("httpfs")
    db.load_extension("httpfs")
    db.execute(f"""
        CREATE SECRET(
            TYPE s3,
            ENDPOINT '{config.r2_endpoint_url}',
            KEY_ID '{config.r2_access_key_id}',
            SECRET '{config.r2_secret_access_key}',
            REGION '{config.r2_region}',
            URL_STYLE 'path'
        );
    """)
    db.install_extension("ducklake")
    db.execute(f"""
        ATTACH
            'ducklake:postgres:host={config.ducklake_host} port={config.ducklake_port} dbname={config.ducklake_database}'
        AS lake (DATA_PATH 's3://{config.r2_lake_bucket}');
    """)  # noqa: E501
    db.execute("COPY FROM DATABASE sde_raw TO DATABASE lake;")

    shutil.rmtree(sde_dir, ignore_errors=True)
