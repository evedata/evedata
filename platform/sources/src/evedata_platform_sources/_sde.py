import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

from evedata_platform_core.utils._r2 import (
    r2_download,
    r2_get_json_object,
    r2_key_exists,
    r2_upload,
    r2_upload_dir,
)
from evedata_platform_sources._exceptions import (
    SDEArchiveExistsError,
    SDEArchiveNotFoundError,
    SDENotArchivedError,
)
from evedata_platform_utils.http import download
from evedata_platform_utils.zip import extract

if TYPE_CHECKING:
    from types_boto3_s3 import S3Client as R2Client

ARCHIVE_PREFIX = "ccp/sde"
ARCHIVE_LATEST_VERSION_KEY = f"{ARCHIVE_PREFIX}/latest.json"
ARCHIVE_DATA_FILENAME = "data.zip"
ARCHIVE_DATA_CHANGELOG_FILENAME = "data-changelog.jsonl"
ARCHIVE_SCHEMA_CHANGELOG_FILENAME = "schema-changelog.yaml"
SDE_LATEST_VERSION_URL = (
    "https://developers.eveonline.com/static-data/tranquility/latest.jsonl"
)
SDE_DATA_BASE_URL = (
    "https://developers.eveonline.com/static-data/tranquility/eve-online-static-data"
)
SDE_DATA_CHANGELOG_URL = (
    "https://developers.eveonline.com/static-data/tranquility/changes"
)
SDE_SCHEMA_CHANGELOG_URL = (
    "https://developers.eveonline.com/static-data/tranquility/schema-changelog.yaml"
)


def latest_sde_version() -> int:
    """Get the latest SDE version from CCP.

    Returns:
        The latest SDE version.
    """
    resp = httpx.get(SDE_LATEST_VERSION_URL)
    resp.raise_for_status()
    data = resp.json()
    return int(data["buildNumber"])


def sde_data_changelog_url(version: int | None = None) -> str:
    """Get the SDE changelog URL for a given version.

    Args:
        version: The version to get the URL for. If None, get the latest.

    Returns:
        The SDE changelog URL.
    """
    if version is None:
        version = latest_sde_version()
    return f"{SDE_DATA_CHANGELOG_URL}/{version}.jsonl"


def sde_data_url(version: int | None = None) -> str:
    """Get the SDE data URL for a given version.

    Args:
        version: The version to get the URL for. If None, get the latest.

    Returns:
        The SDE data URL.
    """
    if version is None:
        version = latest_sde_version()
    return f"{SDE_DATA_BASE_URL}-{version}-jsonl.zip"


def download_sde(output_dir: Path, version: int | None = None) -> None:
    """Download the SDE data, data changelog, and schema changelog.

    Args:
        output_dir: The directory to download the SDE data to.
        version: The version to download. If None, download the latest.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    if version is None:
        version = latest_sde_version()

    filename_prefix = f"sde-{version}"
    download(
        sde_data_url(version), output_dir / f"{filename_prefix}-{ARCHIVE_DATA_FILENAME}"
    )
    download(
        sde_data_changelog_url(version),
        output_dir / f"{filename_prefix}-{ARCHIVE_DATA_CHANGELOG_FILENAME}",
    )
    download(
        SDE_SCHEMA_CHANGELOG_URL,
        output_dir / f"{filename_prefix}-{ARCHIVE_SCHEMA_CHANGELOG_FILENAME}",
    )


def latest_archive_version(*, bucket: str, r2: "R2Client") -> int | None:
    """Get the latest SDE version from the lake.

    Returns:
        The latest archive version or None if no archives.
    """
    if r2_key_exists(bucket=bucket, key=ARCHIVE_LATEST_VERSION_KEY, r2=r2):
        return r2_get_json_object(bucket=bucket, key=ARCHIVE_LATEST_VERSION_KEY, r2=r2)[
            "version"
        ]
    return None


def archive_exists(version: int, *, bucket: str, r2: "R2Client") -> bool:
    """Check if an archive exists in R2.

    Args:
        version: The SDE version to check.
        bucket: The archive bucket.
        r2: The R2 client.
    """
    return r2_key_exists(
        bucket=bucket,
        key=f"{ARCHIVE_PREFIX}/sde-{version}-{ARCHIVE_DATA_FILENAME}",
        r2=r2,
    )


def create_archive(
    version: int | None = None,
    *,
    bucket: str,
    r2: "R2Client",
    exist_ok: bool = True,
    force: bool = False,
) -> int:
    """Archive the SDE data, data changelog, and schema changelog.

    Args:
        version: The SDE version to archive.
        bucket: The archive bucket.
        force: Overwrite existing version.
        r2: The R2 client.
        exist_ok: If True, do not raise if the version is already archived.
    """
    version = version or latest_sde_version()

    if archive_exists(version, bucket=bucket, r2=r2) and not force:
        if exist_ok:
            return version
        raise SDEArchiveExistsError(version)

    with tempfile.TemporaryDirectory() as tmp_dir:
        download_sde(Path(tmp_dir), version)
        r2_upload_dir(bucket, ARCHIVE_PREFIX, Path(tmp_dir), r2=r2)
        r2_upload(bucket, ARCHIVE_LATEST_VERSION_KEY, {"version": version}, r2=r2)

    return version


def download_archive(
    output_dir: Path,
    version: int | None = None,
    *,
    bucket: str,
    r2: "R2Client",
    force: bool = False,
) -> None:
    """Download and uncompress an archive.

    Args:
        output_dir: The directory to download to.
        version: The SDE version to archive.
        bucket: The archive bucket.
        force: Overwrite existing download.
        r2: The R2 client.
    """
    version = version or latest_archive_version(bucket=bucket, r2=r2)
    if not version:
        raise SDENotArchivedError()

    if not archive_exists(version, bucket=bucket, r2=r2):
        raise SDEArchiveNotFoundError(version)

    if output_dir.exists() and not force:
        m = "Output directory exists: "
        raise FileExistsError(m, output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    filename_prefix = f"sde-{version}"
    r2_download(
        bucket,
        f"{ARCHIVE_PREFIX}/{filename_prefix}-{ARCHIVE_DATA_FILENAME}",
        output_dir,
        r2,
    )
    r2_download(
        bucket,
        f"{ARCHIVE_PREFIX}/{filename_prefix}-{ARCHIVE_DATA_CHANGELOG_FILENAME}",
        output_dir,
        r2,
    )
    r2_download(
        bucket,
        f"{ARCHIVE_PREFIX}/{filename_prefix}-{ARCHIVE_SCHEMA_CHANGELOG_FILENAME}",
        output_dir,
        r2,
    )


def stage_archive(
    stage_dir: Path,
    version: int | None = None,
    *,
    bucket: str,
    r2: "R2Client",
    force: bool = False,
) -> Path:
    """Stage an archive."""
    if version is not None and not archive_exists(version, bucket=bucket, r2=r2):
        raise SDEArchiveNotFoundError(version)

    version = version or latest_archive_version(bucket=bucket, r2=r2)
    if not version:
        raise SDENotArchivedError()

    version_dir = stage_dir / Path(str(version))
    if version_dir.exists() and force:
        shutil.rmtree(version_dir)
    elif version_dir.exists():
        m = "Staging directory exists: "
        raise FileExistsError(m, version_dir)

    sde_dir = version_dir / "sde"
    sde_dir.mkdir(parents=True, exist_ok=True)

    download_archive(version_dir, version, bucket=bucket, r2=r2, force=force)
    extract(version_dir / f"sde-{version}-data.zip", sde_dir)
    return sde_dir


if __name__ == "__main__":
    from rich import print as rprint

    from evedata_platform_core import Configuration
    from evedata_platform_core.utils._r2 import r2_client_from_config

    config = Configuration()  # pyright: ignore[reportCallIssue]
    r2 = r2_client_from_config(config)
    bucket = config.sources_bucket

    rprint("Latest SDE version:", latest_sde_version())
    archive_version = latest_archive_version(bucket=bucket, r2=r2)
    if not archive_version:
        rprint("No archives found, archiving latest version...")
        archive_version = create_archive(bucket=bucket, r2=r2)
        rprint("Archived version:", archive_version)
    else:
        rprint("Latest archive version:", archive_version)

    rprint("Staging archive...")
    stage_archive(
        config.sde_staging_dir,
        version=archive_version,
        bucket=bucket,
        r2=r2,
        force=True,
    )
    rprint("Staged archive in:", config.sde_staging_dir / str(archive_version))
