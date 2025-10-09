"""Provides DLT sources for HDE data."""

from typing import TYPE_CHECKING, Any

import dlt

from evedata_platform_extract._utils._sources import get_json_resource

if TYPE_CHECKING:
    from pathlib import Path


_RESOURCE_EXCLUDES = [
    "agenttypes",
    "attributeorders",
    "blueprints",
    "dbuffs",
    "dogmaunits",
    "dynamicitemattributes",
    "localization_dgmattributes",
    "localization_languages",
    "skinmaterialnames",
    "skinmaterials",
    "skins",
    "typematerials",
]


@dlt.source
def hde(path: "Path", version: int) -> Any:
    """A DLT source for a local HDE directory."""
    files = path.glob("*.json")
    resources: list[Any] = []

    for file in files:
        name = file.stem
        if name in _RESOURCE_EXCLUDES:
            continue

        resource = dlt.resource(
            get_json_resource(file),
            name=name,
            parallelized=True,
            write_disposition="append",
        )
        resource = resource.add_map(lambda r: r | {"_hde_version": version})
        resources.append(resource)

    yield from resources
