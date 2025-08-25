from pathlib import Path  # noqa: TC003
from typing import Annotated

import typer
from typer import Typer

from evedata_reference._paths import default_hde_path, default_sde_path

cmd = Typer(name="extract")


@cmd.callback()
def callback() -> None:
    """Extract reference data from raw sources."""


@cmd.command(name="esi")
def esi_cmd(
    *,
    destination: Annotated[
        str | None, typer.Option(help="Name of the destination to extract to.")
    ] = None,
    only: Annotated[
        str | None, typer.Option(help="Comma-separated list of resources to extract.")
    ] = None,
    except_: Annotated[
        str | None,
        typer.Option(
            "--except",
            help="Comma-separated list of resources to exclude from extraction.",
        ),
    ] = None,
) -> None:
    """Extract raw data from the ESI API."""
    from evedata_reference._dlt._pipelines import build_pipeline  # noqa: PLC0415
    from evedata_reference._dlt._sources import esi  # noqa: PLC0415

    source = esi()
    if only:
        resource_names = [name.strip() for name in only.split(",")]
        source = source.with_resources(*resource_names)
    if except_:
        excluded_names = [name.strip() for name in except_.split(",")]
        resource_names = [r for r in source.resources if r not in excluded_names]
        source = source.with_resources(*resource_names)

    build_pipeline("esi", "esi_raw", destination_name=destination).run(
        source, loader_file_format="parquet", refresh="drop_sources"
    )


@cmd.command(name="hde")
def hde_cmd(
    *,
    source_path: Annotated[
        "Path | None",
        typer.Option(
            help="Path to the HDE data directory",
            default_factory=default_hde_path,
            dir_okay=True,
            file_okay=False,
            exists=True,
            resolve_path=True,
            readable=True,
        ),
    ],
    destination: Annotated[
        str | None, typer.Option(help="Name of the destination to extract to.")
    ] = None,
    only: Annotated[
        str | None, typer.Option(help="Comma-separated list of resources to extract.")
    ] = None,
    except_: Annotated[
        str | None,
        typer.Option(
            "--except",
            help="Comma-separated list of resources to exclude from extraction.",
        ),
    ] = None,
) -> None:
    """Extract raw data from the HDE."""
    from evedata_reference._dlt._naming import (  # noqa: PLC0415
        hde as hde_naming_convention,
    )
    from evedata_reference._dlt._pipelines import build_pipeline  # noqa: PLC0415
    from evedata_reference._dlt._sources import hde  # noqa: PLC0415

    source = hde(source_path)
    if only:
        resource_names = [name.strip() for name in only.split(",")]
        source = source.with_resources(*resource_names)
    if except_:
        excluded_names = [name.strip() for name in except_.split(",")]
        resource_names = [r for r in source.resources if r not in excluded_names]
        source = source.with_resources(*resource_names)

    build_pipeline(
        "hde",
        "hde_raw",
        destination_name=destination,
        naming_convention_module=hde_naming_convention,
    ).run(source, loader_file_format="parquet", refresh="drop_sources")


@cmd.command(name="sde")
def sde_cmd(
    *,
    source_path: Annotated[
        "Path | None",
        typer.Option(
            help="Path to the SDE data directory",
            default_factory=default_sde_path,
            dir_okay=True,
            file_okay=False,
            exists=True,
            resolve_path=True,
            readable=True,
        ),
    ],
    destination: Annotated[
        str | None, typer.Option(help="Name of the destination to extract to.")
    ] = None,
    only: Annotated[
        str | None, typer.Option(help="Comma-separated list of resources to extract.")
    ] = None,
    except_: Annotated[
        str | None,
        typer.Option(
            "--except",
            help="Comma-separated list of resources to exclude from extraction.",
        ),
    ] = None,
) -> None:
    """Extract raw data from the SDE."""
    from evedata_reference._dlt._pipelines import build_pipeline  # noqa: PLC0415
    from evedata_reference._dlt._sources import sde  # noqa: PLC0415

    source = sde(source_path)
    if only:
        resource_names = [name.strip() for name in only.split(",")]
        source = source.with_resources(*resource_names)
    if except_:
        excluded_names = [name.strip() for name in except_.split(",")]
        resource_names = [r for r in source.resources if r not in excluded_names]
        source = source.with_resources(*resource_names)

    build_pipeline(
        "sde",
        "sde_raw",
        destination_name=destination,
    ).run(source, loader_file_format="parquet", refresh="drop_sources")
