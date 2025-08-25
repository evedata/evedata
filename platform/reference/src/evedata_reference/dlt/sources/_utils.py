from functools import cache, lru_cache
from typing import TYPE_CHECKING, Any

from evedata_utils.yaml import load_yaml_file

from evedata_reference._utils import (
    load_json_with_normalized_id_keys,
    load_yaml_with_normalized_id_keys,
)

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path

    from dlt.extract import DltResource

    from ._types import FileResourceConfig


def process_data(
    data: dict[str, Any],
    config: "FileResourceConfig",
    names: dict[int, str] | None = None,
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
    return final_data


def get_json_resource(
    path: "Path", config: "FileResourceConfig", names: dict[int, str] | None = None
) -> "Generator[dict[str, Any]]":
    names = names or {}
    for data in load_json_with_normalized_id_keys(path):
        yield process_data(data, config, names)


def get_yaml_resource(
    path: "Path", config: "FileResourceConfig", names: dict[int, str] | None = None
) -> "Generator[dict[str, Any]]":
    names = names or {}
    for data in load_yaml_with_normalized_id_keys(path):
        yield process_data(data, config, names)


def get_yaml_resource_glob(
    path: "Path",
    glob: str,
    config: "FileResourceConfig",
    names: dict[int, str] | None = None,
) -> "Generator[dict[str, Any]]":
    names = names or {}
    for file_path in path.glob(glob):
        for data in load_yaml_with_normalized_id_keys(file_path):
            data["_path"] = str(file_path)
            yield process_data(data, config, names)


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
