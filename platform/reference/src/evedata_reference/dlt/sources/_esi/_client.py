from pathlib import Path
from typing import Any

import hishel
import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from evedata_reference._constants import USER_AGENT
from evedata_reference._exceptions import ESIErrorLimitReachedError
from evedata_reference._utils._datetime import http_date_to_iso8601

_RETRIABLE_EXCEPTIONS = httpx.RequestError


class ESIClient:
    def __init__(
        self,
        user_agent: str | None = None,
        http_client: httpx.Client | None = None,
        cache_storage: hishel.BaseStorage | None = None,
    ) -> None:
        self._user_agent = user_agent or USER_AGENT

        if not http_client:
            cache_storage = cache_storage or hishel.FileStorage(base_path=Path.cwd() / ".http_cache")
            http_client = hishel.CacheClient(headers={"User-Agent": self._user_agent}, storage=cache_storage)
        self._http_client = http_client

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=1, max=10),
        retry=retry_if_exception_type(_RETRIABLE_EXCEPTIONS),
        reraise=True,
    )
    def get(self, path: str, query: dict[str, Any] | None = None) -> tuple[dict[str, Any] | list[Any], dict[str, Any]]:
        def raise_for_error_limit(response: httpx.Response) -> None:
            if response.headers.get("x-esi-error-limit-remain") == "0":
                raise ESIErrorLimitReachedError()

        query = query or {}

        initial_response = self._http_client.get(f"https://esi.evetech.net{path}")
        response_metadata = {
            "compatibility_date": initial_response.headers.get("x-compatibility-date"),
            "expires": http_date_to_iso8601(initial_response.headers.get("expires")),
            "last_modified": http_date_to_iso8601(initial_response.headers.get("last-modified")),
        }
        raise_for_error_limit(initial_response)
        initial_response.raise_for_status()

        if "x-pages" not in initial_response.headers:
            return initial_response.json(), response_metadata

        total_pages = int(initial_response.headers["x-pages"])
        all_data = initial_response.json()
        for page in range(2, total_pages + 1):
            page_query = query.copy()
            page_query["page"] = page
            paged_response = self._http_client.get(f"https://esi.evetech.net{path}", params=page_query)
            raise_for_error_limit(paged_response)
            paged_response.raise_for_status()
            all_data.extend(paged_response.json())

        return all_data, response_metadata
