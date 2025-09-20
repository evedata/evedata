"""Utility functions for handling zip files."""

import zipfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def extract(zip_file: "Path", extract_to: "Path") -> None:
    """Extract a zip file to a specified directory.

    Args:
        zip_file: The path to the zip file.
        extract_to: The directory to extract the contents to.
    """
    extract_to.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_file, "r") as z:
        z.extractall(extract_to)
