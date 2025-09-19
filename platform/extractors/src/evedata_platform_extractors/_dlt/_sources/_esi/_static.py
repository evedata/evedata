"""Provides a DLT source for ESI data."""

from typing import TYPE_CHECKING, Any, cast

import dlt

from evedata_platform_extractors._utils import ESIClient
from evedata_platform_extractors._utils._sources import before_load, process_data

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from dlt.extract import DltResource

    from evedata_platform_extractors._types import ESIResourceConfig


_RESOURCE_CONFIGS: dict[str, "ESIResourceConfig"] = {
    "ancestries": {
        "path": "/universe/ancestries",
        "hints": {"primary_key": "id"},
    },
    "asteroid_belts": {
        "depends_on": "solar_systems",
        "path": "/universe/asteroid_belts/%s",
        "ids_fn": lambda r, _: [
            id_ for p in r.get("planets", []) for id_ in p.get("asteroid_belts", [])
        ],
        "include_id_in_record": True,
        "hints": {"primary_key": "id"},
    },
    "bloodlines": {
        "path": "/universe/bloodlines",
        "rename_columns": {"bloodline_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "categories": {
        "ids_path": "/universe/categories",
        "path": "/universe/categories/%s",
        "rename_columns": {"category_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "constellations": {
        "ids_path": "/universe/constellations",
        "path": "/universe/constellations/%s",
        "rename_columns": {"constellation_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "dogma_attributes": {
        "ids_path": "/dogma/attributes",
        "path": "/dogma/attributes/%s",
        "rename_columns": {"attribute_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "dogma_effects": {
        "ids_path": "/dogma/effects",
        "path": "/dogma/effects/%s",
        "rename_columns": {"effect_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "factions": {
        "path": "/universe/factions",
        "rename_columns": {"faction_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "graphics": {
        "ids_path": "/universe/graphics",
        "path": "/universe/graphics/%s",
        "rename_columns": {"graphic_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "groups": {
        "ids_path": "/universe/groups",
        "path": "/universe/groups/%s",
        "rename_columns": {"group_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "market_groups": {
        "ids_path": "/markets/groups",
        "path": "/markets/groups/%s",
        "rename_columns": {"market_group_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "moons": {
        "depends_on": "solar_systems",
        "path": "/universe/moons/%s",
        "ids_fn": lambda r, _: [
            id_ for p in r.get("planets", []) for id_ in p.get("moons", [])
        ],
        "rename_columns": {"moon_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "npc_corporations": {
        "ids_path": "/corporations/npccorps",
        "path": "/corporations/%s",
        "include_id_in_record": True,
        "hints": {"primary_key": "id"},
    },
    "npc_corporation_icons": {
        "ids_path": "/corporations/npccorps",
        "path": "/corporations/%s/icons",
        "include_id_in_record": True,
        "hints": {"primary_key": "id"},
    },
    "planets": {
        "depends_on": "solar_systems",
        "path": "/universe/planets/%s",
        "ids_fn": lambda r, _: [p["planet_id"] for p in r.get("planets", [])],
        "rename_columns": {"planet_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "races": {
        "path": "/universe/races",
        "rename_columns": {"race_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "regions": {
        "ids_path": "/universe/regions",
        "path": "/universe/regions/%s",
        "rename_columns": {"region_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "solar_systems": {
        "ids_path": "/universe/systems",
        "path": "/universe/systems/%s",
        "rename_columns": {"system_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "stargates": {
        "depends_on": "solar_systems",
        "path": "/universe/stargates/%s",
        "ids_fn": lambda r, _: r.get("stargates", []),
        "rename_columns": {"stargate_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "stars": {
        "depends_on": "solar_systems",
        "path": "/universe/stars/%s",
        "ids_fn": lambda r, _: [r["star_id"]] if "star_id" in r else [],
        "include_id_in_record": True,
        "hints": {"primary_key": "id"},
    },
    "stations": {
        "depends_on": "solar_systems",
        "path": "/universe/stations/%s",
        "ids_fn": lambda r, _: r.get("stations", []),
        "rename_columns": {"station_id": "id"},
        "hints": {"primary_key": "id"},
    },
    "types": {
        "ids_path": "/universe/types",
        "path": "/universe/types/%s",
        "rename_columns": {"type_id": "id"},
        "hints": {"primary_key": "id"},
    },
}


@dlt.source
def esi_static() -> Any:
    """DLT source for ESI static data."""
    client = ESIClient()

    def get_esi_resource(config: "ESIResourceConfig") -> "Generator[dict[str, Any]]":
        if ids_path := config.get("ids_path"):
            ids, _ = client.get(ids_path)
            for id_ in ids:
                path = config["path"] % id_
                data: dict[str, Any]
                data, response_metadata = cast(
                    "tuple[dict[str, Any], dict[str, Any]]", client.get(path)
                )
                data["_esi"] = response_metadata
                if config.get("include_id_in_record"):
                    data["id"] = id_
                yield process_data(data, config)
        else:
            path = config["path"]
            all_data, response_metadata = cast(
                "tuple[list[dict[str, Any]], dict[str, Any]]", client.get(path)
            )
            for data in all_data:
                data["_esi"] = response_metadata
                yield process_data(data, config)

    def get_esi_transformer(
        name: str, config: "ESIResourceConfig"
    ) -> "Callable[[Any], Generator[dict[str, Any]]]":
        ids_fn = config.get("ids_fn")
        if not ids_fn:
            msg = f"Resource {name} depends on another resource but has no ids_fn"
            raise ValueError(msg)

        def transform_fn(record: dict[str, Any]) -> "Generator[dict[str, Any]]":
            ids = ids_fn(record, config)
            for id_ in ids:
                path = config["path"] % id_
                data, response_metadata = cast(
                    "tuple[dict[str, Any], dict[str, Any]]", client.get(path)
                )
                data["_esi"] = response_metadata
                if config.get("include_id_in_record"):
                    data["id"] = id_
                yield process_data(data, config)

        return transform_fn

    resources: dict[str, DltResource] = {}

    resource_configs = {
        k: v for k, v in _RESOURCE_CONFIGS.items() if "depends_on" not in v
    }
    for resource_name, resource_config in resource_configs.items():
        hints = resource_config.get("hints", {})
        resource = dlt.resource(
            get_esi_resource(resource_config),
            name=resource_name,
            parallelized=True,
            write_disposition="replace",
        ).apply_hints(**hints)
        resource = before_load(resource, resource_config)
        resources[resource_name] = resource

    transform_configs = {
        k: v for k, v in _RESOURCE_CONFIGS.items() if "depends_on" in v
    }
    for resource_name, resource_config in transform_configs.items():
        dependency = resources[resource_config["depends_on"]]
        hints = resource_config.get("hints", {})
        resource = dlt.transformer(
            get_esi_transformer(resource_name, resource_config),
            data_from=dependency,
            name=resource_name,
            parallelized=True,
            write_disposition="replace",
        ).apply_hints(**hints)
        resource = before_load(resource, resource_config)
        resources[resource_name] = resource

    yield from resources.values()
