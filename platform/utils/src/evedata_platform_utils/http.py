"""Utilities for making HTTP requests."""

from typing import TYPE_CHECKING

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

if TYPE_CHECKING:
    from pathlib import Path

EVEDATA_USER_AGENT = "EVEData/1.0 (admin@evedata.io; +https://github.com/evedata)"


@retry(
    retry=retry_if_exception_type(httpx.RequestError),
    stop=stop_after_attempt(3),
    wait=wait_fixed(10),
)
def download(url: str, download_path: "Path") -> None:
    """Download a file from a URL to a given path."""
    with httpx.stream(
        "GET", url, headers={"User-Agent": EVEDATA_USER_AGENT}
    ) as response:
        response.raise_for_status()
        with download_path.open("wb") as f:
            for chunk in response.iter_bytes():
                f.write(chunk)
