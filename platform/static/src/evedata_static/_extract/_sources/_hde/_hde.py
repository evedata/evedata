"""Provides DLT sources for HDE data."""

from typing import TYPE_CHECKING, Any

import dlt

from evedata_static._utils._sources import before_load, get_json_resource

from ._resources import *  # noqa: F403  # noqa: F403

if TYPE_CHECKING:
    from pathlib import Path

    from evedata_static._types import FileResourceConfig


_RESOURCE_CONFIGS: dict[str, "FileResourceConfig"] = {
    "accounting_entry_types": {"hints": {"primary_key": "id"}},
    "agent_types": {"hints": {"primary_key": "key"}},
    "attribute_orders": {},
    "clone_states": {"hints": {"primary_key": "id"}},
    "compressible_types": {"hints": {"primary_key": "key"}},
    "dogma_effect_categories": {"hints": {"primary_key": "key"}},
    "dogma_units": {"hints": {"primary_key": "id"}},
    "dynamic_item_attributes": {"hints": {"primary_key": "id"}},
    "expert_systems": {"hints": {"primary_key": "id"}},
    "graphic_material_sets": {"hints": {"primary_key": "id"}},
    "industry_activities": {"hints": {"primary_key": "activity_id"}},
    "industry_assembly_lines": {"hints": {"primary_key": "id"}},
    "industry_installation_types": {"hints": {"primary_key": "type_id"}},
    "industry_modifier_sources": {"hints": {"primary_key": "id"}},
    "industry_target_filters": {"hints": {"primary_key": "id"}},
    "localization_dogma_attributes": {"hints": {"primary_key": "id"}},
    "localization_languages": {},
    "repackaged_volumes": {"hints": {"primary_key": "key"}},
    "school_map": {"hints": {"primary_key": "id"}},
    "schools": {"hints": {"primary_key": "id"}},
    "skill_plans": {"hints": {"primary_key": "id"}},
    "skin_material_names": {"hints": {"primary_key": "key"}},
    "skin_materials": {"hints": {"primary_key": "skin_material_id"}},
    "station_standings_restrictions": {"hints": {"primary_key": "id"}},
    "type_materials": {"hints": {"primary_key": "id"}},
}
_RESOURCE_NAMES: dict[str, str] = {
    "accountingentrytypes": "accounting_entry_types",
    "agenttypes": "agent_types",
    "attributeorders": "attribute_orders",
    "clonestates": "clone_states",
    "compressibletypes": "compressible_types",
    "dogmaeffectcategories": "dogma_effect_categories",
    "dogmaunits": "dogma_units",
    "dynamicitemattributes": "dynamic_item_attributes",
    "expertsystems": "expert_systems",
    "graphicmaterialsets": "graphic_material_sets",
    "industryactivities": "industry_activities",
    "industryassemblylines": "industry_assembly_lines",
    "industryinstallationtypes": "industry_installation_types",
    "industrymodifiersources": "industry_modifier_sources",
    "industrytargetfilters": "industry_target_filters",
    "localization_dgmattributes": "localization_dogma_attributes",
    "localization_languages": "localization_languages",
    "repackagedvolumes": "repackaged_volumes",
    "schoolmap": "school_map",
    "skillplans": "skill_plans",
    "skinmaterialnames": "skin_material_names",
    "skinmaterials": "skin_materials",
    "stationstandingsrestrictions": "station_standings_restrictions",
    "typematerials": "type_materials",
}


@dlt.source
def hde(path: "Path") -> Any:
    """A DLT source for a local HDE directory."""
    files = path.glob("*.json")
    resources: list[Any] = []

    for file in files:
        default_name = file.stem
        name = _RESOURCE_NAMES.get(default_name, default_name)
        if name in ["attribute_orders"]:
            continue

        resource_config = _RESOURCE_CONFIGS.get(name, {})
        hints = resource_config.get("hints", {})
        resource = dlt.resource(
            get_json_resource(file, path, resource_config),
            name=name,
            parallelized=True,
            write_disposition="replace",
        ).apply_hints(**hints)
        resource = before_load(resource, resource_config)
        resources.append(resource)

    yield from resources
