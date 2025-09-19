"""Provides a DLT source for ESI region market orders."""

import asyncio
from typing import TYPE_CHECKING, Any

import dlt
import hishel
import httpx
from evedata_platform_utils.datetime import http_date_to_datetime
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from evedata_platform_extractors._constants import MARKET_REGION_IDS, USER_AGENT
from evedata_platform_extractors._exceptions import ESIErrorLimitReachedError

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from pathlib import Path


@dlt.resource(name="esi_public_market_orders", write_disposition="append")
async def get_esi_public_market_orders_resource(
    cache_path: "Path",
) -> "AsyncGenerator[list[dict[str, Any]]]":
    """DLT resource for ESI public market orders."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=1, max=10),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=True,
    )
    async def fetch_page(path: str, page: int) -> httpx.Response:
        response = await client.get(
            f"https://esi.evetech.net{path}", params={"page": page}
        )
        if response.headers.get("x-esi-error-limit-remain") == "0":
            raise ESIErrorLimitReachedError()
        response.raise_for_status()
        return response

    cache_storage = hishel.AsyncFileStorage(base_path=cache_path)
    async with hishel.AsyncCacheClient(
        headers={"User-Agent": USER_AGENT}, storage=cache_storage
    ) as client:
        for region_id in MARKET_REGION_IDS:
            path = f"/markets/{region_id}/orders/"

            first_page = await fetch_page(path, 1)
            metadata = {
                "expires": http_date_to_datetime(first_page.headers.get("expires")),
                "last_modified": http_date_to_datetime(
                    first_page.headers.get("last-modified")
                ),
            }

            yield [o | metadata for o in first_page.json()]

            total_pages = int(first_page.headers.get("x-pages", "1"))
            if total_pages <= 1:
                continue

            page_tasks = [fetch_page(path, page) for page in range(2, total_pages + 1)]
            async for task in asyncio.as_completed(page_tasks):
                response = await task
                yield response.json() | metadata


@dlt.source
async def esi_public_market_orders(cache_path: "Path") -> Any:
    """DLT source for ESI public market orders."""
    return [get_esi_public_market_orders_resource(cache_path)]
