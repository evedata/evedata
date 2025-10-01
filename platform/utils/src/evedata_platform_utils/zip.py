"""Utility functions for handling zip files."""

import zipfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def compress(zip_file: "Path", source_dir: "Path") -> None:
    """Compress a directory into a zip file.

    Args:
        zip_file: The path to the zip file to create.
        source_dir: The directory to compress.
    """
    zip_file.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as z:
        for file in source_dir.rglob("*"):
            z.write(file, file.relative_to(source_dir))


def extract(zip_file: "Path", extract_to: "Path") -> None:
    """Extract a zip file to a specified directory.

    Args:
        zip_file: The path to the zip file.
        extract_to: The directory to extract the contents to.
    """
    extract_to.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_file, "r") as z:
        z.extractall(extract_to)
