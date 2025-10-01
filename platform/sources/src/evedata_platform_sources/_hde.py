"""Provides utilities for sourcing from the Hoboleaks Data Export (HDE)."""

import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import httpx

from evedata_platform_core.utils._r2 import (
    r2_client_from_config,
    r2_download,
    r2_list_keys,
    r2_upload,
)
from evedata_platform_sources._constants import HDE_BASE_URL, HDE_META_URL
from evedata_platform_utils.http import download
from evedata_platform_utils.json import load_json_file
from evedata_platform_utils.zip import compress

if TYPE_CHECKING:
    from evedata_platform_core import Configuration

ARCHIVE_PREFIX = "hde"


def current_archived_hde_version(config: "Configuration") -> str | None:
    """Get the current archived HDE version.

    Returns:
        The current archived HDE version.
    """
    client = r2_client_from_config(config)
    all_versions = [
        k
        for k in sorted(
            r2_list_keys(client, config.sources_bucket, ARCHIVE_PREFIX), reverse=True
        )
        if k.endswith(".zip")
    ]
    if not all_versions:
        return None
    return all_versions[0].split("/")[-1].removeprefix("hde-").removesuffix(".zip")


def archive_prefix_for_version(version: str) -> str:
    """Get the R2 archive key for the given version."""
    return f"{ARCHIVE_PREFIX}/hde-{version}"


def archive_current_hde_version(
    config: "Configuration", *, overwrite: bool = False
) -> str:
    """Archive the current HDE version to R2."""
    current_hoboleaks_version = current_hoboleaks_hde_version()
    current_archive_version = current_archived_hde_version(config)
    r2 = r2_client_from_config(config)

    if (
        current_archive_version
        and current_hoboleaks_version == current_archive_version
        and not overwrite
    ):
        return current_archive_version

    with tempfile.TemporaryDirectory(
        f"evedata-hde-archive-{current_hoboleaks_version}"
    ) as tmp_dir:
        tmp_path = Path(tmp_dir)
        download_hoboleaks_hde(tmp_path)

        r2 = r2_client_from_config(config)
        bucket = config.sources_bucket

        try:
            stem = f"hde-{current_hoboleaks_version}"
            r2_upload(
                r2, bucket, f"{ARCHIVE_PREFIX}/{stem}.zip", tmp_path / f"{stem}.zip"
            )
            r2_upload(
                r2,
                bucket,
                f"{ARCHIVE_PREFIX}/{stem}.meta.json",
                tmp_path / f"{stem}.meta.json",
            )
        except r2.exceptions.ClientError as e:
            msg = f"Failed to upload HDE version {current_hoboleaks_version} to R2: {e}"
            raise RuntimeError(msg) from e
        else:
            current_archive_version = current_hoboleaks_version

    return current_archive_version


def download_archived_hde(
    config: "Configuration",
    output_dir: "Path | None" = None,
    version: str | None = None,
) -> None:
    """Download the archived HDE zip file.

    Args:
        config: The platform configuration.
        output_dir: Path to download to.
        version: The version to download. If None, download the latest version.
    """
    if version is None:
        version = current_archived_hde_version(config)
        if version is None:
            msg = "No archived SDE versions found in R2"
            raise FileNotFoundError(msg)

    archive_prefix = archive_prefix_for_version(version)

    output_dir = output_dir or config.cache_dir / "sde" / version
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    r2 = r2_client_from_config(config)
    meta_path = output_dir / "hde.meta.json"
    zip_path = output_dir / "hde.zip"
    try:
        r2_download(r2, config.sources_bucket, f"{archive_prefix}.zip", zip_path)
        r2_download(r2, config.sources_bucket, f"{archive_prefix}.meta.json", meta_path)
    except r2.exceptions.ClientError as e:
        msg = f"Failed to download HDE version {version} from R2: {e}"
        raise RuntimeError(msg) from e


def stage_archived_hde(
    config: "Configuration",
    output_dir: "Path | None" = None,
    version: str | None = None,
    *,
    overwrite: bool = False,
) -> Path:
    """Download and extract the archived HDE zip file.

    Args:
        config: The platform configuration.
        output_dir: Path to extract to.
        version: The version to download. If None, download the latest version.
        ignore_existing: If True, do nothing if the output directory exists.
        overwrite: If True, overwrite the output directory if it exists.

    Returns:
        The path to the extracted HDE.
    """
    if version is None:
        version = current_archived_hde_version(config)
        if version is None:
            msg = "No archived HDE versions found in R2"
            raise ValueError(msg)

    output_dir = output_dir or config.hde_staging_dir / version
    output_dir = output_dir.resolve()

    if output_dir.exists() and not overwrite:
        return output_dir

    if output_dir.exists() and overwrite:
        output_dir.rename(output_dir.with_suffix(".bak"))

    output_dir.mkdir(parents=True, exist_ok=True)

    download_dir = config.cache_dir / "hde" / version
    download_dir.mkdir(parents=True, exist_ok=True)
    download_archived_hde(config, download_dir, version)

    zip_path = download_dir / "hde.zip"
    try:
        with zipfile.ZipFile(zip_path, "r", zipfile.ZIP_DEFLATED) as zf:
            zf.extractall(output_dir)
    except zipfile.BadZipFile as e:
        shutil.rmtree(output_dir, ignore_errors=True)
        output_dir.with_suffix(".bak").rename(output_dir)

        msg = f"Downloaded HDE zip file is corrupted: {e}"
        raise RuntimeError(msg) from e
    finally:
        shutil.rmtree(download_dir, ignore_errors=True)
        shutil.rmtree(output_dir.with_suffix(".bak"), ignore_errors=True)

    return output_dir


def current_hoboleaks_hde_version() -> str:
    """Get the current Hoboleaks HDE version.

    Returns:
        The current Hoboleaks HDE version.
    """
    meta = current_hoboleaks_hde_meta()
    return meta["revision"]


def current_hoboleaks_hde_meta() -> dict[str, Any]:
    """Get the current Hoboleaks HDE metadata.

    Returns:
        The current Hoboleaks HDE metadata.
    """
    resp = httpx.get(HDE_META_URL)
    resp.raise_for_status()
    return resp.json()


def download_hoboleaks_hde(output_dir: "Path") -> None:
    """Download the current Hoboleaks HDE to the given directory.

    Args:
        output_dir: The directory to download the HDE to.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    meta_path = output_dir / "meta.json"
    download(HDE_META_URL, meta_path)
    meta = cast("dict[str, Any]", load_json_file(meta_path))
    version = meta["revision"]

    file_urls = [HDE_BASE_URL + "/" + filename for filename in meta["files"]]
    (output_dir / "hde").mkdir(parents=True, exist_ok=True)
    for file_url in file_urls:
        filename = file_url.split("/")[-1]
        file_path = output_dir / "hde" / filename
        download(file_url, file_path)

    output_filename = f"hde-{version}.zip"
    zip_path = output_dir / output_filename
    compress(zip_path, output_dir / "hde")

    meta_path.rename(output_dir / f"hde-{version}.meta.json")
