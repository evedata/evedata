from typing import TYPE_CHECKING, Any, cast

from evedata_utils.json import load_json_file

from ._normalize_id_keys import NormalizedDict, normalize_id_keys

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path


def is_int(value: str) -> bool:
    """Check if a string can be converted to an integer."""
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def load_json_with_normalized_id_keys(
    path: "str | Path",
) -> "Generator[dict[str, Any]]":
    data = load_json_file(path)
    if isinstance(data, list):
        for item in data:
            yield cast("NormalizedDict", normalize_id_keys(item))
    elif all(is_int(k) and not isinstance(v, dict) for k, v in data.items()):
        for id_, value in data.items():
            yield {"id": int(id_), "value": value}
    elif all(is_int(k) for k in data):
        for id_, item in data.items():
            yield {"id": int(id_), **cast("NormalizedDict", normalize_id_keys(item))}
    else:
        yield normalize_id_keys(data)
