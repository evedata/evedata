"""Provides utilities for sourcing from the Static Data Export (SDE)."""

import hashlib
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

from evedata_platform_core.utils._r2 import (
    r2_client_from_config,
    r2_download,
    r2_list_keys,
    r2_upload,
)
from evedata_platform_sources._constants import (
    SDE_TRANQUILITY_CHECKSUMS_URL,
    SDE_TRANQUILITY_ZIP_URL,
)
from evedata_platform_utils.datetime import http_date_to_date
from evedata_platform_utils.http import download

if TYPE_CHECKING:
    from evedata_platform_core import Configuration


ARCHIVE_PREFIX = "ccp/sde"


def current_archived_sde_version(config: "Configuration") -> str | None:
    """Get the current archived SDE version.

    Returns:
        The current archived SDE version.
    """
    client = r2_client_from_config(config)
    all_versions = [
        k
        for k in sorted(
            r2_list_keys(client, config.r2_sources_bucket, ARCHIVE_PREFIX), reverse=True
        )
        if k.endswith(".zip")
    ]
    if not all_versions:
        return None
    return all_versions[0].split("/")[-1].removeprefix("sde-").removesuffix(".zip")


def archive_prefix_for_version(version: str) -> str:
    """Get the R2 archive key for the given version."""
    return f"{ARCHIVE_PREFIX}/sde-{version}"


def archive_current_sde_version(
    config: "Configuration", *, overwrite: bool = False
) -> str:
    """Archive the current SDE version to R2.

    Args:
        config: The platform configuration.
        overwrite: If True, overwrite the existing archive if it exists.

    Returns:
        The archived SDE version.
    """
    current_ccp_version = current_ccp_sde_version()
    current_archive_version = current_archived_sde_version(config)
    r2 = r2_client_from_config(config)

    if (
        current_archive_version
        and current_ccp_version == current_archive_version
        and not overwrite
    ):
        return current_archive_version

    with tempfile.TemporaryDirectory(
        f"evedata-sde-archive-{current_ccp_version}"
    ) as tmp_dir:
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
            msg = (
                "SDE zip file does not match expected checksum. "
                f"Expected: {expected_checksum}, Actual: {actual_checksum}"
            )
            raise RuntimeError(msg)

        r2 = r2_client_from_config(config)
        bucket = config.r2_sources_bucket

        try:
            r2_upload(r2, bucket, f"{ARCHIVE_PREFIX}/{stem}.zip", zip_path)
            r2_upload(r2, bucket, f"{ARCHIVE_PREFIX}/{stem}.checksums", checksums_path)
        except r2.exceptions.ClientError as e:
            msg = f"Failed to upload SDE version {current_ccp_version} to R2: {e}"
            raise RuntimeError(msg) from e
        else:
            current_archive_version = current_ccp_version

    return current_archive_version


def download_archived_sde(
    config: "Configuration",
    output_dir: "Path | None" = None,
    version: str | None = None,
) -> None:
    """Download the archived SDE zip file.

    Args:
        config: The platform configuration.
        output_dir: Path to download to.
        version: The version to download. If None, download the latest version.
    """
    if version is None:
        version = current_archived_sde_version(config)
        if version is None:
            msg = "No archived SDE versions found in R2"
            raise FileNotFoundError(msg)

    archive_prefix = archive_prefix_for_version(version)

    output_dir = output_dir or config.cache_dir / "sde" / version
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    r2 = r2_client_from_config(config)
    checksums_path = output_dir / "sde.checksums"
    zip_path = output_dir / "sde.zip"
    try:
        r2_download(r2, config.r2_sources_bucket, f"{archive_prefix}.zip", zip_path)
        r2_download(
            r2, config.r2_sources_bucket, f"{archive_prefix}.checksums", checksums_path
        )
    except r2.exceptions.ClientError as e:
        msg = f"Failed to download SDE version {version} from R2: {e}"
        raise RuntimeError(msg) from e


def stage_archived_sde(
    config: "Configuration",
    output_dir: "Path | None" = None,
    version: str | None = None,
    *,
    overwrite: bool = False,
) -> Path:
    """Download and extract the archived SDE zip file.

    Args:
        config: The platform configuration.
        output_dir: Path to extract to.
        version: The version to download. If None, download the latest version.
        ignore_existing: If True, do nothing if the output directory exists.
        overwrite: If True, overwrite the output directory if it exists.

    Returns:
        The path to the extracted SDE.
    """
    if version is None:
        version = current_archived_sde_version(config)
        if version is None:
            msg = "No archived SDE versions found in R2"
            raise ValueError(msg)

    output_dir = output_dir or config.sde_staging_dir / version
    output_dir = output_dir.resolve()

    if output_dir.exists() and not overwrite:
        return output_dir

    if output_dir.exists() and overwrite:
        output_dir.rename(output_dir.with_suffix(".bak"))

    output_dir.mkdir(parents=True, exist_ok=True)

    download_dir = config.cache_dir / "sde" / version
    download_dir.mkdir(parents=True, exist_ok=True)
    download_archived_sde(config, download_dir, version)

    zip_path = download_dir / "sde.zip"
    try:
        with zipfile.ZipFile(zip_path, "r", zipfile.ZIP_DEFLATED) as zf:
            zf.extractall(output_dir)
    except zipfile.BadZipFile as e:
        shutil.rmtree(output_dir, ignore_errors=True)
        output_dir.with_suffix(".bak").rename(output_dir)

        msg = f"Downloaded SDE zip file is corrupted: {e}"
        raise RuntimeError(msg) from e
    finally:
        shutil.rmtree(download_dir, ignore_errors=True)
        shutil.rmtree(output_dir.with_suffix(".bak"), ignore_errors=True)

    return output_dir


def current_ccp_sde_version() -> str:
    """Get the current SDE version date.

    Returns:
        The current SDE version.
    """
    resp = httpx.get(SDE_TRANQUILITY_CHECKSUMS_URL)
    resp.raise_for_status()

    if "last-modified" not in resp.headers:
        msg = "No Last-Modified header in SDE checksum response"
        raise ValueError(msg)

    version = http_date_to_date(resp.headers["last-modified"])
    if not version:
        msg = "Invalid Last-Modified header in SDE checksum response"
        raise ValueError(msg)

    return version.strftime("%Y%m%d")


def download_ccp_sde_checksums(output_file: "Path") -> None:
    """Download the SDE checksums from the official SDE endpoint.

    Returns:
        A dictionary mapping file names to their checksums.
    """
    download(SDE_TRANQUILITY_CHECKSUMS_URL, output_file)


def parse_ccp_sde_checksums(file_path: "Path") -> dict[str, str]:
    """Parse the SDE checksums file.

    Args:
        file_path: Path to the checksums file.

    Returns:
        A dictionary mapping file names to their checksums.
    """
    checksums: dict[str, str] = {}
    lines = file_path.read_text().splitlines()
    for line in lines:
        md5, filename = line.strip().split()
        checksums[filename] = md5.lower()
    return checksums


def download_ccp_sde_zip(output_file: "Path") -> None:
    """Download the SDE from the official SDE endpoint."""
    download(SDE_TRANQUILITY_ZIP_URL, output_file)


def calculate_ccp_sde_checksum(file_path: "Path") -> str:
    """Calculate the MD5 checksum of the SDE zip file.

    Args:
        file_path (Path | str):
            Path to the SDE zip file.

    Returns:
        str: The MD5 checksum of the file.
    """
    md5 = hashlib.md5()  # noqa: S324
    with zipfile.ZipFile(file_path, "r", zipfile.ZIP_DEFLATED) as zf:
        filenames = zf.namelist()
        for filename in filenames:
            md5.update(zf.read(filename))
    return md5.hexdigest().lower()


def verify_ccp_sde(zip_path: "Path", checksums_path: "Path") -> tuple[str, str, bool]:
    """Verify the SDE file against the provided checksums.

    Args:
        zip_path: Path to the SDE zip file.
        checksums_path: Path to the checksums file.

    Returns:
        True if the file matches the checksum, False otherwise.
    """
    checksums = parse_ccp_sde_checksums(checksums_path)
    expected = checksums.get("sde.zip", "")
    actual = calculate_ccp_sde_checksum(zip_path)
    return (expected, actual, expected == actual)
