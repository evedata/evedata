import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import typer
from typer import Typer

from evedata_platform_core.utils._r2 import r2_client_from_config, r2_upload
from evedata_platform_sources._sde import (
    ARCHIVE_PREFIX,
    current_archived_sde_version,
    current_ccp_sde_version,
    download_ccp_sde_checksums,
    download_ccp_sde_zip,
    stage_archived_sde,
    verify_ccp_sde,
)

if TYPE_CHECKING:
    from evedata_platform_admin_core import AdminState

cmd = Typer(name="sde")


@cmd.callback()
def callback():
    """Manage Static Data Export (SDE) archives."""


@cmd.command(name="archive")
def archive_cmd(
    *,
    ctx: typer.Context,
    force: Annotated[bool, typer.Option(help="Overwrite existing archive")] = False,
) -> None:
    """Archive the current SDE version."""
    state: AdminState = ctx.obj
    config = state.config
    err = state.err

    current_ccp_version = current_ccp_sde_version()
    current_archive_version = current_archived_sde_version(config)

    if current_ccp_version == current_archive_version and not force:
        err.print(
            f"SDE version {current_ccp_version} is already archived. "
            "Use --force to re-archive."
        )
        raise typer.Exit(0)

    with tempfile.TemporaryDirectory("evedatactl-sources-sde-archive") as tmp_dir:
        tmp_path = Path(tmp_dir)
        stem = f"sde-{current_ccp_version}"

        checksums_path = tmp_path / f"{stem}.checksums"
        download_ccp_sde_checksums(checksums_path)

        zip_path = tmp_path / f"{stem}.zip"
        download_ccp_sde_zip(zip_path)

        expected_checksum, actual_checksum, is_valid = verify_ccp_sde(
            zip_path, checksums_path
        )
        if not is_valid:
            err.print(
                "SDE zip file does not match expected checksum. "
                f"Expected: {expected_checksum}, Actual: {actual_checksum}"
            )
            raise typer.Exit(1)

        r2 = r2_client_from_config(config)
        bucket = config.r2_sources_bucket

        r2_upload(r2, bucket, f"{ARCHIVE_PREFIX}/{stem}.zip", zip_path)
        r2_upload(r2, bucket, f"{ARCHIVE_PREFIX}/{stem}.checksums", checksums_path)


@cmd.command(name="stage")
def stage_cmd(
    *,
    ctx: typer.Context,
    output_dir: Annotated[
        Path | None,
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
        typer.Option(help="SDE version to stage. Defaults to latest archived."),
    ] = None,
    force: Annotated[
        bool, typer.Option(help="Overwrite existing staged version")
    ] = False,
) -> None:
    """Stage an archived SDE version by downloading and extracting it."""
    state: AdminState = ctx.obj
    config = state.config
    err = state.err
    out = state.out

    if version is None:
        version = current_archived_sde_version(config)
        if version is None:
            err.print("No archived SDE versions found.")
            raise typer.Exit(1)

    output_dir = output_dir or config.state_dir / "sde" / version

    out.print(f"Staging SDE version {version} to {output_dir}")
    stage_archived_sde(config, output_dir, version, overwrite=force)
