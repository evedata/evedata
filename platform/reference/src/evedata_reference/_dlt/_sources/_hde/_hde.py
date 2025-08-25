"""Provides DLT sources for HDE data."""

from pathlib import Path
from typing import TYPE_CHECKING, Any

import dlt

from evedata_reference._dlt._sources._sde._resources._blueprints import (
    blueprints_config as sde_blueprints_config,
)
from evedata_reference._dlt._sources._sde._resources._skins import (
    skins_config as sde_skins_config,
)
from evedata_reference._dlt._sources._sde._resources._type_materials import (
    type_materials_config as sde_type_materials_config,
)
from evedata_reference._utils._sources import before_load, get_json_resource

from ._resources import *  # noqa: F403  # noqa: F403

if TYPE_CHECKING:
    from evedata_reference._types import FileResourceConfig


_RESOURCE_CONFIGS: dict[str, "FileResourceConfig"] = {
    "accounting_entry_types": {"hints": {"primary_key": "id"}},
    "agent_types": {
        "rename_columns": {"value": "name"},
        "hints": {"primary_key": "id"},
    },
    "blueprints": sde_blueprints_config,
    "clone_states": clone_states_config,  # noqa: F405
    "compressible_types": {
        "rename_columns": {"value": "compressedTypeID"},
        "hints": {"primary_key": "id"},
    },
    "dbuffs": dbuffs_config,  # noqa: F405
    "dogma_effect_categories": {
        "rename_columns": {"value": "name"},
        "hints": {"primary_key": "id"},
    },
    "dogma_units": {"hints": {"primary_key": "id"}},
    "expert_systems": expert_systems_config,  # noqa: F405
    "graphic_material_sets": {"hints": {"primary_key": "id"}},
    "industry_activities": {"hints": {"primary_key": "id"}},
    "industry_assembly_lines": industry_assembly_lines_config,  # noqa: F405
    "industry_installation_types": industry_installation_types_config,  # noqa: F405
    "industry_modifier_sources": industry_modifier_sources_config,  # noqa: F405
    "industry_target_filters": industry_target_filters_config,  # noqa: F405
    "localization_dogma_attributes": {"hints": {"primary_key": "id"}},
    "mutaplasmids": mutaplasmids_config,  # noqa: F405
    "repackaged_volumes": {
        "rename_columns": {"id": "typeID", "value": "volume"},
        "hints": {"primary_key": "typeID"},
    },
    "school_map": {"hints": {"primary_key": "id"}},
    "schools": schools_config,  # noqa: F405
    "skill_plans": skill_plans_config,  # noqa: F405
    "skin_material_names": {
        "rename_columns": {"id": "materialID", "value": "name"},
        "hints": {"primary_key": "materialID"},
    },
    "skin_materials": {"hints": {"primary_key": "id"}},
    "skins": sde_skins_config,
    "station_standings_restrictions": station_standings_restrictions_config,  # noqa: F405
    "type_materials": sde_type_materials_config,
}
_RESOURCE_NAMES: dict[str, str] = {
    "accountingentrytypes": "accounting_entry_types",
    "agenttypes": "agent_types",
    "attributeorders": "attribute_orders",
    "clonestates": "clone_states",
    "compressibletypes": "compressible_types",
    "dogmaeffectcategories": "dogma_effect_categories",
    "dogmaunits": "dogma_units",
    "dynamicitemattributes": "mutaplasmids",
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


def _default_hde_path() -> Path:
    return Path.cwd() / "data" / "hde"


@dlt.source
def hde(path: str | Path | None = None) -> Any:
    """A DLT source for a local HDE directory."""
    path = path or dlt.config.get("hde_path", Path) or _default_hde_path()
    hde_path = Path(path).resolve()
    files = hde_path.glob("*.json")
    resources: list[Any] = []

    for file in files:
        default_name = file.stem
        name = _RESOURCE_NAMES.get(default_name, default_name)
        if name in ["attribute_orders", "localization_languages", "meta"]:
            continue

        config = _RESOURCE_CONFIGS.get(name, {})
        hints = config.get("hints", {})
        resource = dlt.resource(
            get_json_resource(file, config),
            name=name,
            parallelized=True,
            write_disposition="replace",
        ).apply_hints(**hints)
        resource = before_load(resource, config)
        resources.append(resource)

    yield from resources
