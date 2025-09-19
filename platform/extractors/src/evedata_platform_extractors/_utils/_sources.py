from functools import cache, lru_cache
from typing import TYPE_CHECKING, Any

from evedata_platform_utils.yaml import load_yaml_file

from evedata_platform_extractors._utils import (
    load_json_with_normalized_id_keys,
    load_yaml_with_normalized_id_keys,
)

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

    from dlt.extract import DltResource
    from dlt.sources import DltSource

    from evedata_platform_extractors._types import FileResourceConfig


def process_data(
    data: dict[str, Any],
    config: "FileResourceConfig",
    names: dict[int, str] | None = None,
    path: "Path | None" = None,
    base_path: "Path | None" = None,
) -> dict[str, Any]:
    final_data = data
    if "before_extract" in config:
        for func in config["before_extract"]:
            final_data = func(final_data)
    if "rename_columns" in config:
        final_data = {
            config["rename_columns"].get(k, k): v for k, v in final_data.items()
        }
    if names and config.get("name_from_inv_names"):
        final_data["name"] = names.get(final_data["id"], "Name Unknown")
    if path:
        final_data["_dlt_resource_path"] = str(path)
    if base_path:
        final_data["_dlt_base_path"] = str(base_path)
    return final_data


def get_json_resource(
    path: "Path",
    root_path: "Path",
    config: "FileResourceConfig",
    names: dict[int, str] | None = None,
) -> "Generator[dict[str, Any]]":
    names = names or {}
    for data in load_json_with_normalized_id_keys(path):
        yield process_data(data, config, names, path.relative_to(root_path))


def get_yaml_resource(
    path: "Path",
    root_path: "Path",
    config: "FileResourceConfig",
    names: dict[int, str] | None = None,
) -> "Generator[dict[str, Any]]":
    names = names or {}
    for data in load_yaml_with_normalized_id_keys(path):
        yield process_data(data, config, names, path.relative_to(root_path))


def get_yaml_resource_glob(
    search_path: "Path",
    glob: str,
    config: "FileResourceConfig",
    names: dict[int, str] | None = None,
) -> "Generator[dict[str, Any]]":
    names = names or {}
    for file_path in search_path.glob(glob):
        for data in load_yaml_with_normalized_id_keys(file_path):
            yield process_data(
                data, config, names, file_path.relative_to(search_path), search_path
            )


def before_load(resource: "DltResource", config: "FileResourceConfig") -> "DltResource":
    if "before_load" in config:
        for func in config["before_load"]:
            resource = resource.add_map(func)
    return resource


@cache
def inv_names(path: "Path") -> dict[int, str]:
    data = load_yaml_with_normalized_id_keys(path)
    return {e["itemID"]: e["itemName"] for e in data}


@lru_cache
def constellation_id_from_solar_system_path(path: "Path") -> int:
    data: dict[str, Any] = load_yaml_file(path.parent.parent / "constellation.yaml")
    return data["constellationID"]


@lru_cache
def region_id_from_constellation_path(path: "Path") -> int:
    data: dict[str, Any] = load_yaml_file(path.parent.parent / "region.yaml")
    return data["regionID"]


@lru_cache
def region_id_from_solar_system_path(path: "Path") -> int:
    constellation_path = path.parent.parent / "constellation.yaml"
    return region_id_from_constellation_path(constellation_path)


def position_dict_from_array(arr: list[float]) -> dict[str, float]:
    return {"x": arr[0], "y": arr[1], "z": arr[2]}


def filter_resources(
    source: "DltSource",
    *,
    include: list[str] | None = None,
    exclude: list[str] | None = None,
) -> "DltSource":
    if include:
        return source.with_resources(*include)
    if exclude:
        resource_names = [r for r in source.resources if r not in exclude]
        return source.with_resources(*resource_names)
    return source
