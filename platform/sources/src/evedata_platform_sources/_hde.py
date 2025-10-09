"""Provides utilities for sourcing from the Hoboleaks Data Export (HDE)."""

import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import httpx

from evedata_platform_core.utils._r2 import (
    r2_download,
    r2_get_json_object,
    r2_key_exists,
    r2_upload,
    r2_upload_dir,
)
from evedata_platform_sources._exceptions import (
    HDEArchiveExistsError,
    HDEArchiveNotFoundError,
    HDENotArchivedError,
)
from evedata_platform_utils.http import download
from evedata_platform_utils.json import load_json_file
from evedata_platform_utils.zip import compress, extract

if TYPE_CHECKING:
    from types_boto3_s3 import S3Client as R2Client


ARCHIVE_PREFIX = "hoboleaks/hde"
ARCHIVE_LATEST_VERSION_KEY = f"{ARCHIVE_PREFIX}/latest.json"
ARCHIVE_DATA_FILENAME = "data.zip"
ARCHIVE_META_FILENAME = "meta.json"
HDE_BASE_URL = "https://sde.hoboleaks.space/tq"
HDE_META_URL = f"{HDE_BASE_URL}/meta.json"


def latest_hde_version() -> int:
    """Get the current Hoboleaks HDE version.

    Returns:
        The current Hoboleaks HDE version.
    """
    meta = latest_hde_meta()
    return int(meta["revision"])


def latest_hde_meta() -> dict[str, Any]:
    """Get the current Hoboleaks HDE metadata.

    Returns:
        The current Hoboleaks HDE metadata.
    """
    resp = httpx.get(HDE_META_URL)
    resp.raise_for_status()
    return resp.json()


def download_hde(output_dir: "Path") -> None:
    """Download the current Hoboleaks HDE to the given directory.

    Args:
        output_dir: The directory to download the HDE to.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    meta_path = output_dir / ARCHIVE_META_FILENAME
    download(HDE_META_URL, meta_path)
    meta = cast("dict[str, Any]", load_json_file(meta_path))
    version = int(meta["revision"])

    file_urls = [HDE_BASE_URL + "/" + filename for filename in meta["files"]]
    (output_dir / "hde").mkdir(parents=True, exist_ok=True)
    for file_url in file_urls:
        filename = file_url.split("/")[-1]
        file_path = output_dir / "hde" / filename
        download(file_url, file_path)

    filename_prefix = f"hde-{version}"
    output_filename = f"{filename_prefix}-{ARCHIVE_DATA_FILENAME}"
    zip_path = output_dir / output_filename
    compress(zip_path, output_dir / "hde")

    meta_path.rename(output_dir / f"{filename_prefix}-{ARCHIVE_META_FILENAME}")
    shutil.rmtree(output_dir / "hde", ignore_errors=True)


def latest_archive_version(*, bucket: str, r2: "R2Client") -> int | None:
    """Get the current archived HDE version.

    Returns:
        The current archived HDE version.
    """
    if r2_key_exists(bucket=bucket, key=ARCHIVE_LATEST_VERSION_KEY, r2=r2):
        return int(
            r2_get_json_object(bucket=bucket, key=ARCHIVE_LATEST_VERSION_KEY, r2=r2)[
                "version"
            ]
        )
    return None


def archive_exists(version: int, *, bucket: str, r2: "R2Client") -> bool:
    """Check if the given HDE version is archived in R2.

    Args:
        version: The version to check.
        bucket: The R2 bucket to check in.
        r2: The R2 client to use.

    Returns:
        True if the version is archived, False otherwise.
    """
    return r2_key_exists(
        bucket=bucket,
        key=f"{ARCHIVE_PREFIX}/hde-{version}-{ARCHIVE_DATA_FILENAME}",
        r2=r2,
    )


def create_archive(
    *, bucket: str, r2: "R2Client", exist_ok: bool = True, force: bool = False
) -> int:
    """Archive the current HDE version to R2."""
    version = latest_hde_version()

    if archive_exists(int(version), bucket=bucket, r2=r2) and not force:
        if exist_ok:
            return version
        raise HDEArchiveExistsError(version)

    with tempfile.TemporaryDirectory() as tmp_dir:
        download_hde(Path(tmp_dir))
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
        raise HDENotArchivedError()

    if not archive_exists(version, bucket=bucket, r2=r2):
        raise HDEArchiveNotFoundError(version)

    if output_dir.exists() and not force:
        m = "Output directory exists: "
        raise FileExistsError(m, output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    filename_prefix = f"hde-{version}"
    r2_download(
        bucket,
        f"{ARCHIVE_PREFIX}/{filename_prefix}-{ARCHIVE_DATA_FILENAME}",
        output_dir,
        r2,
    )
    r2_download(
        bucket,
        f"{ARCHIVE_PREFIX}/{filename_prefix}-{ARCHIVE_META_FILENAME}",
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
        raise HDEArchiveNotFoundError(version)

    version = version or latest_archive_version(bucket=bucket, r2=r2)
    if not version:
        raise HDENotArchivedError()

    version_dir = stage_dir / Path(str(version))
    if version_dir.exists() and force:
        shutil.rmtree(version_dir)
    elif version_dir.exists():
        m = "Staging directory exists: "
        raise FileExistsError(m, version_dir)

    hde_dir = version_dir / "hde"
    hde_dir.mkdir(parents=True, exist_ok=True)

    download_archive(version_dir, version, bucket=bucket, r2=r2, force=force)
    extract(version_dir / f"hde-{version}-data.zip", hde_dir)
    return hde_dir
