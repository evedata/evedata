from typing import TYPE_CHECKING, Any, cast

from evedata_utils.yaml import load_yaml_file

from ._normalize_id_keys import normalize_id_keys

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path


def load_yaml_with_normalized_id_keys(
    path: "str | Path",
) -> "Generator[dict[str, Any]]":
    data: dict[int, dict[str, Any]] | dict[str, Any] | list[dict[str, Any]] = (
        load_yaml_file(path)
    )
    if isinstance(data, list):
        for item in data:
            yield normalize_id_keys(item)
    elif all(isinstance(k, str) for k in data):
        yield cast("dict[str, Any]", normalize_id_keys(data))
    else:
        for id_, item in data.items():
            yield {"id": id_, **normalize_id_keys(item)}
