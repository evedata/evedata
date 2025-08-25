from pathlib import Path
from typing import TYPE_CHECKING, Any

import orjson as json

from ._normalize_id_keys import normalize_id_keys

if TYPE_CHECKING:
    from collections.abc import Generator


def is_int(value: str) -> bool:
    """Check if a string can be converted to an integer."""
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def load_json_with_normalized_id_keys(
    path: str | Path,
) -> "Generator[dict[str, Any]]":
    full_path = Path(path).resolve()
    with full_path.open("r", encoding="utf-8") as file:
        data: dict[str, dict[str, Any]] | dict[str, Any] | list[dict[str, Any]] = json.loads(file.read())
    if isinstance(data, list):
        for item in data:
            yield normalize_id_keys(item)
    elif all(is_int(k) and not isinstance(v, dict) for k, v in data.items()):
        for id_, value in data.items():
            yield {"id": int(id_), "value": value}
    elif all(is_int(k) for k in data):
        for id_, item in data.items():
            yield {"id": int(id_), **normalize_id_keys(item)}
    else:
        yield normalize_id_keys(data)
