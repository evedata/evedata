from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_faction(record: dict[str, Any]) -> dict[str, Any]:
    if "memberRaces" in record:
        new_member_races = [
            {"faction_id": record["id"], "race_id": entry}
            for entry in record["memberRaces"]
        ]
        record["memberRaces"] = new_member_races
    return record


factions_config: "ResourceConfig" = {
    "before_load": [_before_load_faction],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "memberRaces": make_nested_hints(primary_key=["faction_id", "race_id"])
        },
    },
}
