from typing import TYPE_CHECKING, Annotated

import orjson as json
import typer
from typer import Typer

from evedata_static.sde import (
    current_sde_version,
    download_sde,
    download_sde_checksums,
    unpack_sde,
)

if TYPE_CHECKING:
    from evedata_admin_core import AdminState

cmd = Typer()


@cmd.command(name="download")
def download_cmd(
    *,
    ctx: typer.Context,
    source: Annotated[
        str, typer.Argument(metavar="hde|sde", help="The source to download.")
    ],
) -> None:
    """Download raw reference sources."""
    state: AdminState = ctx.obj
    config = state.config

    if source == "sde":
        sde_version = current_sde_version()
        sde_stem = f"sde-{sde_version.isoformat()}"
        sde_dir = config.sde_path / f"date={sde_version.isoformat()}"
        sde_dir.mkdir(exist_ok=True)
        sde_checksums = download_sde_checksums()

        sde_checksums_file = sde_dir / f"{sde_stem}-checksums.json"
        sde_checksums_file.write_bytes(json.dumps(sde_checksums))

        sde_archive_file = sde_dir / f"{sde_stem}.zip"
        download_sde(sde_archive_file)

        sde_unpack_dir = sde_dir / "sde"
        unpack_sde(sde_archive_file, sde_unpack_dir)
