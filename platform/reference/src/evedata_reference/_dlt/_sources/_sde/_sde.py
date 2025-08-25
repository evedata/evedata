from pathlib import Path
from typing import TYPE_CHECKING, Any

import dlt

from evedata_reference._utils._sources import (
    before_load,
    get_yaml_resource,
    get_yaml_resource_glob,
    inv_names,
)

from ._resources import *  # noqa: F403

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


_RESOURCE_CONFIGS: dict[str, "ResourceConfig"] = {
    "agents": {"hints": {"primary_key": "id"}},
    "agents_in_space": {"hints": {"primary_key": "id"}},
    "ancestries": {"hints": {"primary_key": "id"}},
    "bloodlines": {"hints": {"primary_key": "id"}},
    "blueprints": blueprints_config,  # noqa: F405
    "categories": {"hints": {"primary_key": "id"}},
    "certificates": certificates_config,  # noqa: F405
    "character_attributes": {"hints": {"primary_key": "id"}},
    "constellations": constellations_config,  # noqa: F405
    "contraband_types": contraband_types_config,  # noqa: F405
    "control_tower_resources": control_tower_resources_config,  # noqa: F405
    "corporation_activities": {"hints": {"primary_key": "id"}},
    "dogma_attribute_categories": {"hints": {"primary_key": "id"}},
    "dogma_attributes": {"hints": {"primary_key": "id"}},
    "dogma_effects": {
        "hints": {
            "primary_key": "id",
            "columns": {"modifierInfo": {"data_type": "json"}},
        }
    },
    "factions": factions_config,  # noqa: F405
    "graphics": graphics_config,  # noqa: F405
    "groups": {"hints": {"primary_key": "id"}},
    "icons": {"hints": {"primary_key": "id"}},
    "flags": {"rename_columns": {"flagID": "id"}, "hints": {"primary_key": "id"}},
    "items": {"rename_columns": {"itemID": "id"}, "hints": {"primary_key": "id"}},
    "item_names": {
        "rename_columns": {"itemID": "id", "itemName": "name"},
        "hints": {"primary_key": "id"},
    },
    "item_positions": {
        "rename_columns": {"itemID": "id"},
        "hints": {"primary_key": "id"},
    },
    "item_unique_names": {
        "rename_columns": {"itemID": "id", "itemName": "name"},
        "hints": {"primary_key": "id"},
    },
    "landmarks": landmarks_config,  # noqa: F405
    "market_groups": {"hints": {"primary_key": "id"}},
    "meta_groups": meta_groups_config,  # noqa: F405
    "npc_corporation_divisions": {"hints": {"primary_key": "id"}},
    "npc_corporations": npc_corporations_config,  # noqa: F405
    "planet_resources": {"hints": {"primary_key": "id"}},
    "planet_schematics": planet_schematics_config,  # noqa: F405
    "races": races_config,  # noqa: F405
    "regions": regions_config,  # noqa: F405
    "research_agents": research_agents_config,  # noqa: F405
    "skin_licenses": {"hints": {"primary_key": "id"}},
    "skin_materials": {"hints": {"primary_key": "id"}},
    "skins": skins_config,  # noqa: F405
    "solar_systems": solar_systems_config,  # noqa: F405
    "sovereignty_upgrades": {"hints": {"primary_key": "id"}},
    "station_operations": station_operations_config,  # noqa: F405
    "station_services": {"hints": {"primary_key": "id"}},
    "stations": stations_config,  # noqa: F405
    "tournament_rule_sets": tournament_rule_sets_config,  # noqa: F405
    "type_dogma": type_dogma_config,  # noqa: F405
    "type_materials": type_materials_config,  # noqa: F405
    "types": types_config,  # noqa: F405
}
_RESOURCE_NAMES: dict[str, str] = {
    "agentsInSpace": "agents_in_space",
    "characterAttributes": "character_attributes",
    "constellation": "constellations",
    "contrabandTypes": "contraband_types",
    "controlTowerResources": "control_tower_resources",
    "corporationActivities": "corporation_activities",
    "dogmaAttributeCategories": "dogma_attribute_categories",
    "dogmaAttributes": "dogma_attributes",
    "dogmaEffects": "dogma_effects",
    "graphicIDs": "graphics",
    "iconIDs": "icons",
    "invFlags": "flags",
    "invItems": "items",
    "invNames": "item_names",
    "invPositions": "item_positions",
    "invUniqueNames": "item_unique_names",
    "marketGroups": "market_groups",
    "metaGroups": "meta_groups",
    "npcCorporationDivisions": "npc_corporation_divisions",
    "npcCorporations": "npc_corporations",
    "planetResources": "planet_resources",
    "planetSchematics": "planet_schematics",
    "region": "regions",
    "researchAgents": "research_agents",
    "skinLicenses": "skin_licenses",
    "skinMaterials": "skin_materials",
    "solarsystem": "solar_systems",
    "sovereigntyUpgrades": "sovereignty_upgrades",
    "staStations": "stations",
    "stationOperations": "station_operations",
    "stationServices": "station_services",
    "tournamentRuleSets": "tournament_rule_sets",
    "typeDogma": "type_dogma",
    "typeMaterials": "type_materials",
}


def _default_sde_path() -> Path:
    return Path.cwd() / "data" / "sde"


@dlt.source
def sde(path: str | Path | None = None) -> Any:
    """A DLT source for the EVE Online Static Data Export (SDE)."""
    path = path or dlt.config.get("sde_path", str) or _default_sde_path()
    sde_path = Path(path).resolve()

    files: list[Path] = []
    files.extend(sde_path.glob("fsd/*.yaml"))
    files.extend(sde_path.glob("bsd/*.yaml"))
    files.append(sde_path / "universe" / "landmarks" / "landmarks.yaml")

    resources: list[Any] = []
    names = inv_names(sde_path / "bsd" / "invNames.yaml")

    for file in files:
        default_name = file.stem
        name = _RESOURCE_NAMES.get(default_name, default_name)
        if name in ["translationLanguages"]:
            continue

        config = _RESOURCE_CONFIGS.get(name, {})
        hints = config.get("hints", {})
        resource = dlt.resource(
            get_yaml_resource(file, config, names),
            name=name,
            parallelized=True,
            write_disposition="replace",
        ).apply_hints(**hints)
        resource = before_load(resource, config)
        resources.append(resource)

    for kind in ["region", "constellation", "solarsystem"]:
        name = _RESOURCE_NAMES.get(kind, kind)
        config = _RESOURCE_CONFIGS.get(name, {})
        hints = config.get("hints", {})
        resource = dlt.resource(
            get_yaml_resource_glob(sde_path, f"universe/**/{kind}.yaml", config, names),
            name=name,
            parallelized=True,
            write_disposition="replace",
        ).apply_hints(**hints)
        resource = before_load(resource, config)
        resource = resource.add_map(
            lambda r: {**r, "_path": str(Path(r["_path"]).relative_to(sde_path))}
        )
        resources.append(resource)

    yield from resources
