from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_npc_corporation(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    if "allowedMemberRaces" in record:
        new_allowed_member_races = [
            {"corporationID": id_, "raceID": race_id}
            for race_id in record["allowedMemberRaces"]
        ]
        record["allowedMemberRaces"] = new_allowed_member_races

    for division in record.get("divisions", []):
        division["corporationID"] = id_
        division["divisionID"] = division.pop("id")

    return record


npc_corporations_config: "ResourceConfig" = {
    "before_load": [_before_load_npc_corporation],
    "hints": {
        "primary_key": "id",
        "columns": [
            {"name": "corporationTrades", "data_type": "json"},
            {"name": "exchangeRates", "data_type": "json"},
            {"name": "investors", "data_type": "json"},
            {"name": "lpOfferTables", "data_type": "json"},
        ],
        "nested_hints": {
            "allowedMemberRaces": make_nested_hints(
                primary_key=["corporationID", "raceID"]
            ),
            "divisions": make_nested_hints(primary_key=["corporationID", "divisionID"]),
        },
    },
}
