from typing import TYPE_CHECKING, Any

import dlt

from evedata_static._utils._sources import (
    before_load,
    get_yaml_resource,
    get_yaml_resource_glob,
    inv_names,
)

from ._resources import (
    constellations_config,
    landmarks_config,
    meta_groups_config,
    npc_corporations_config,
    regions_config,
    solar_systems_config,
)

if TYPE_CHECKING:
    from pathlib import Path

    from evedata_static._types import ResourceConfig


_RESOURCE_CONFIGS: dict[str, "ResourceConfig"] = {
    "constellations": constellations_config,
    "landmarks": landmarks_config,
    "meta_groups": meta_groups_config,
    "npc_corporations": npc_corporations_config,
    "regions": regions_config,
    "solar_systems": solar_systems_config,
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
    "invFlags": "inv_flags",
    "invItems": "inv_items",
    "invNames": "inv_names",
    "invPositions": "inv_positions",
    "invUniqueNames": "inv_unique_names",
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
    "translationLanguages": "translation_languages",
    "typeDogma": "type_dogma",
    "typeMaterials": "type_materials",
}


@dlt.source
def sde(path: "Path") -> Any:
    """A DLT source for the EVE Online Static Data Export (SDE)."""
    files: list[Path] = []
    files.extend(path.glob("fsd/*.yaml"))
    files.extend(path.glob("bsd/*.yaml"))
    files.append(path / "universe" / "landmarks" / "landmarks.yaml")

    resources: list[Any] = []
    names = inv_names(path / "bsd" / "invNames.yaml")

    for file in files:
        default_name = file.stem
        name = _RESOURCE_NAMES.get(default_name, default_name)

        resource_config = _RESOURCE_CONFIGS.get(name, {})
        hints = resource_config.get("hints", {})
        resource = dlt.resource(
            get_yaml_resource(file, path, resource_config, names),
            name=name,
            parallelized=True,
            write_disposition="replace",
        ).apply_hints(**hints)
        resource = before_load(resource, resource_config)
        resources.append(resource)

    for kind in ["region", "constellation", "solarsystem"]:
        name = _RESOURCE_NAMES.get(kind, kind)
        resource_config = _RESOURCE_CONFIGS.get(name, {})
        hints = resource_config.get("hints", {})
        resource = dlt.resource(
            get_yaml_resource_glob(
                path, f"universe/**/{kind}.yaml", resource_config, names
            ),
            name=name,
            parallelized=True,
            write_disposition="replace",
        ).apply_hints(**hints)
        resource = before_load(resource, resource_config)
        resources.append(resource)

    yield from resources
