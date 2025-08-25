from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_contraband_type(record: dict[str, Any]) -> dict[str, Any]:
    type_id = record.get("id")
    factions: list[dict[str, Any]] = record.get("factions", [])
    for faction in factions:
        faction["factionID"] = faction.pop("id")
        faction["typeID"] = type_id
    return record


contraband_types_config: "ResourceConfig" = {
    "before_load": [_before_load_contraband_type],
    "hints": {
        "nested_hints": {
            "factions": make_nested_hints(primary_key=["factionID", "typeID"])
        },
    },
}
