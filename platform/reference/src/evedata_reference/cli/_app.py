from pathlib import Path
from typing import Annotated

import typer
from typer import Typer

app = Typer(name="evedata-reference")


@app.command(name="download-hde")
def download_hde_cmd():
    """Download the latest HDE data."""


@app.command(name="download-sde")
def download_sde_cmd():
    """Download the latest SDE data."""


@app.command(name="load-esi-raw")
def load_esi_raw_cmd(
    *,
    destination: Annotated[
        str | None,
        typer.Option(help="Destination for the DLT pipeline"),
    ] = None,
    resources: Annotated[
        str | None,
        typer.Option(help="ESI resources to include in the pipeline"),
    ] = None,
):
    """Extract, normalize, and load ESI data from the specified path."""
    from evedata_reference.dlt.pipelines import build_pipeline  # noqa: PLC0415
    from evedata_reference.dlt.sources import esi  # noqa: PLC0415

    esi_source = esi()
    if resources:
        resource_names = [f"esi_{r.strip()}" for r in resources.split(",")]
        esi_source = esi_source.with_resources(*resource_names)

    build_pipeline("esi", "esi_raw", destination_name=destination).run(
        esi_source, loader_file_format="parquet"
    )


@app.command(name="load-hde-raw")
def load_hde_raw_cmd(
    *,
    hde_path: Annotated[
        Path | None,
        typer.Option(
            help="Path to the HDE data directory",
            default_factory=lambda: Path.cwd() / "data" / "hde",
            dir_okay=True,
            file_okay=False,
            exists=True,
            resolve_path=True,
            readable=True,
        ),
    ],
    destination: Annotated[
        str | None,
        typer.Option(help="Destination for the DLT pipeline"),
    ] = None,
    resources: Annotated[
        str | None,
        typer.Option(help="HDE Resources to include in the pipeline"),
    ] = None,
):
    """Extract, normalize, and load HDE data from the specified path."""
    from evedata_reference.dlt.naming import (  # noqa: PLC0415
        hde as hde_naming_convention,
    )
    from evedata_reference.dlt.pipelines import build_pipeline  # noqa: PLC0415
    from evedata_reference.dlt.sources import hde  # noqa: PLC0415

    hde_source = hde(hde_path)
    if resources:
        resource_names = [f"hde_{r.strip()}" for r in resources.split(",")]
        hde_source = hde_source.with_resources(*resource_names)

    build_pipeline(
        "hde",
        "hde_raw",
        destination_name=destination,
        naming_convention_module=hde_naming_convention,
    ).run(hde_source, loader_file_format="parquet")


@app.command(name="load-sde-raw")
def load_sde_raw_cmd(
    *,
    sde_path: Annotated[
        Path | None,
        typer.Option(
            help="Path to the SDE data directory",
            default_factory=lambda: Path.cwd() / "data" / "sde",
            dir_okay=True,
            file_okay=False,
            exists=True,
            resolve_path=True,
            readable=True,
        ),
    ],
    destination: Annotated[
        str | None,
        typer.Option(help="Destination for the DLT pipeline"),
    ] = None,
    resources: Annotated[
        str | None,
        typer.Option(help="SDE Resources to include in the pipeline"),
    ] = None,
):
    """Extract, normalize, and load SDE data from the specified path."""
    from evedata_reference.dlt.pipelines import build_pipeline  # noqa: PLC0415
    from evedata_reference.dlt.sources import sde  # noqa: PLC0415

    sde_source = sde(sde_path)
    if resources:
        resource_names = [f"sde_{r.strip()}" for r in resources.split(",")]
        sde_source = sde_source.with_resources(*resource_names)

    build_pipeline("sde", "sde_raw", destination_name=destination).run(
        sde_source, loader_file_format="parquet"
    )
