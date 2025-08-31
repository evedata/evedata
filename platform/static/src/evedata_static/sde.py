"""Provides utilities for downloading and verifying the SDE."""

import hashlib
import zipfile
from email.utils import parsedate_to_datetime
from typing import TYPE_CHECKING, cast

import httpx

from evedata_static._constants import SDE_CHECKSUM_URL, SDE_TRANQUILITY_URL

if TYPE_CHECKING:
    from datetime import date
    from pathlib import Path


def current_sde_version() -> "date":
    """Get the current SDE version date.

    Returns:
        The date of the current SDE version.
    """
    resp = httpx.get(SDE_CHECKSUM_URL)
    resp.raise_for_status()
    return parsedate_to_datetime(resp.headers["Last-Modified"]).date()


def download_sde_checksums() -> dict[str, str]:
    """Download the SDE checksums from the official SDE endpoint.

    Returns:
        A dictionary mapping file names to their checksums.
    """
    resp = httpx.get(SDE_CHECKSUM_URL)
    resp.raise_for_status()

    checksums = {}
    for line in resp.text.splitlines():
        if line.strip():
            checksum, filename = line.split()
            checksums[filename] = checksum

    return cast("dict[str, str]", checksums)


def download_sde(output_file: "Path") -> None:
    """Download the SDE from the official SDE endpoint."""
    with httpx.stream("GET", SDE_TRANQUILITY_URL) as response:
        response.raise_for_status()
        with output_file.open("wb") as f:
            f.writelines(response.iter_bytes())


def unpack_sde(zip_file: "Path", extract_to: "Path") -> None:
    """Unpack the SDE zip file to the specified directory."""
    with zipfile.ZipFile(zip_file, "r") as zf:
        zf.extractall(extract_to)


def calculate_sde_checksum(file_path: "Path") -> str:
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


def verify_sde(file_path: "Path", checksums: dict[str, str]) -> bool:
    """Verify the SDE file against the provided checksums.

    Args:
        file_path: Path to the SDE file.
        checksums: Dictionary of checksums to verify against.

    Returns:
        True if the file matches the checksum, False otherwise.
    """
    expected_checksum = checksums.get("sde.zip")
    return calculate_sde_checksum(file_path) == expected_checksum
