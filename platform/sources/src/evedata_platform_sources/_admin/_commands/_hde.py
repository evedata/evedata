from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING, Annotated

import typer
from typer import Typer

from evedata_platform_sources._hde import (
    archive_current_hde_version,
    current_archived_hde_version,
    current_hoboleaks_hde_version,
    stage_archived_hde,
)

if TYPE_CHECKING:
    from evedata_platform_admin_core import AdminState

cmd = Typer(name="hde")


@cmd.callback()
def callback():
    """Manage Hoboleaks Data Export (HDE) archives."""


@cmd.command(name="archive")
def archive_cmd(
    *,
    ctx: typer.Context,
    force: Annotated[bool, typer.Option(help="Overwrite existing archive")] = False,
) -> None:
    """Archive the current HDE version."""
    state: AdminState = ctx.obj
    config = state.config
    err = state.err

    current_hoboleaks_version = current_hoboleaks_hde_version()
    current_archive_version = current_archived_hde_version(config)
    if current_hoboleaks_version == current_archive_version and not force:
        err.print(
            f"HDE version {current_hoboleaks_version} is already archived. "
            "Use --force to re-archive."
        )
        raise typer.Exit(2)

    archive_current_hde_version(config, overwrite=force)


@cmd.command(name="stage")
def stage_cmd(
    *,
    ctx: typer.Context,
    output_dir: Annotated[
        "Path | None",
        typer.Option(
            "--output",
            "-o",
            help="Directory to stage to",
            dir_okay=True,
            file_okay=False,
            writable=True,
            resolve_path=True,
        ),
    ] = None,
    version: Annotated[
        str | None,
        typer.Option(help="HDE version to stage. Defaults to latest archived."),
    ] = None,
    force: Annotated[
        bool, typer.Option(help="Overwrite existing staged version")
    ] = False,
) -> None:
    """Stage an archived HDE version by downloading and extracting it."""
    state: AdminState = ctx.obj
    config = state.config
    err = state.err
    out = state.out

    if version is None:
        version = current_archived_hde_version(config)
        if version is None:
            err.print("No archived HDE versions found.")
            raise typer.Exit(1)

    output_dir = output_dir or config.hde_staging_dir / version

    out.print(f"Staging HDE version {version} to {output_dir}")
    stage_archived_hde(config, output_dir, version, overwrite=force)
