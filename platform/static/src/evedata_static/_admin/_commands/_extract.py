import re
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import typer
from typer import Typer

from evedata_static._utils._sources import filter_resources

if TYPE_CHECKING:
    from evedata_admin_core import AdminState

cmd = Typer(name="extract")


@cmd.callback()
def callback() -> None:
    """Extract reference data from raw sources."""


@cmd.command(name="hde")
def hde_cmd(  # noqa: PLR0913
    *,
    ctx: typer.Context,
    source_path: Annotated[
        "Path | None",
        typer.Option(
            "--source",
            help="Path to the HDE data directory",
            dir_okay=True,
            file_okay=False,
            exists=True,
            resolve_path=True,
            readable=True,
        ),
    ] = None,
    version: Annotated[
        str | None, typer.Option(help="HDE version date in YYYY-MM-DD format.")
    ] = None,
    destination: Annotated[
        str | None, typer.Option(help="Name of the destination to extract to.")
    ] = None,
    include: Annotated[
        str | None, typer.Option(help="Comma-separated list of resources to include.")
    ] = None,
    exclude: Annotated[
        str | None,
        typer.Option(help="Comma-separated list of resources to exclude."),
    ] = None,
) -> None:
    """Extract raw data from the HDE."""
    from evedata_static._extract._naming import (  # noqa: PLC0415
        hde as hde_naming_convention,
    )
    from evedata_static._extract._pipelines import build_pipeline  # noqa: PLC0415
    from evedata_static._extract._sources import hde  # noqa: PLC0415

    state: AdminState = ctx.obj
    config = state.config

    source_path = source_path or config.hde_path / "latest"
    source_path = Path(source_path).resolve()

    if version is None:
        version_from_path = re.search(r"(\d{4}-\d{2}-\d{2}).*", source_path.name)
        if not version_from_path:
            msg = (
                "Version not specified and could not be inferred from the source path."
            )
            raise ValueError(msg)
        parsed_version = version_from_path.group(1)
        version_date = datetime.strptime(parsed_version, "%Y-%m-%d").date()  # noqa: DTZ007
    else:
        msg = "Version must be in YYYY-MM-DD format."
        raise ValueError(msg)

    source = filter_resources(
        hde(Path(source_path / "hde"), version_date),
        include=include.split(",") if include else None,
        exclude=exclude.split(",") if exclude else None,
    )

    build_pipeline(
        "hde",
        "hde_raw",
        config=config,
        destination_name=destination,
        naming_convention_module=hde_naming_convention,
    ).run(source, loader_file_format="parquet")


@cmd.command(name="sde")
def sde_cmd(  # noqa: PLR0913
    *,
    ctx: typer.Context,
    source_path: Annotated[
        "Path | None",
        typer.Option(
            "--source",
            help="Path to the SDE data directory",
            dir_okay=True,
            file_okay=False,
            exists=True,
            resolve_path=True,
            readable=True,
        ),
    ] = None,
    version: Annotated[
        str | None, typer.Option(help="SDE version date in YYYY-MM-DD format.")
    ] = None,
    destination: Annotated[
        str | None, typer.Option(help="Name of the destination to extract to.")
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
    from evedata_static._extract._pipelines import build_pipeline  # noqa: PLC0415
    from evedata_static._extract._sources import sde  # noqa: PLC0415

    state: AdminState = ctx.obj
    config = state.config

    source_path = source_path or config.sde_path / "latest"
    source_path = Path(source_path).resolve()

    if version is None:
        version_from_path = re.search(r"(\d{4}-\d{2}-\d{2}).*", source_path.name)
        if not version_from_path:
            msg = (
                "Version not specified and could not be inferred from the source path."
            )
            raise ValueError(msg)
        parsed_version = version_from_path.group(1)
        version_date = datetime.strptime(parsed_version, "%Y-%m-%d").date()  # noqa: DTZ007
    else:
        msg = "Version must be in YYYY-MM-DD format."
        raise ValueError(msg)

    source = filter_resources(
        sde(Path(source_path) / "sde", version_date),
        include=include.split(",") if include else None,
        exclude=exclude.split(",") if exclude else None,
    )

    build_pipeline(
        "sde",
        "sde_raw",
        config=config,
        destination_name=destination,
    ).run(source, loader_file_format="parquet")
