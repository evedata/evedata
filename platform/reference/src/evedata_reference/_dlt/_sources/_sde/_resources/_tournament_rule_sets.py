from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_tournament_rule_set(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"] = record.pop("ruleSetID")

    if "bannedGroups" in record:
        record["bannedGroups"] = [
            {"ruleSetID": id_, "groupID": group_id}
            for group_id in record.get("bannedGroups", [])
        ]

    if "bannedTypes" in record:
        record["bannedTypes"] = [
            {"ruleSetID": id_, "typeID": type_id}
            for type_id in record.get("bannedTypes", [])
        ]

    if "points" in record:
        for group_points in record["points"].get("groups", []):
            group_points["ruleSetID"] = id_
        if "groups" in record["points"]:
            record["groupPoints"] = record["points"].pop("groups")

        for type_points in record["points"].get("types", []):
            type_points["ruleSetID"] = id_
        if "types" in record["points"]:
            record["typePoints"] = record["points"].pop("types")
        record.pop("points")

    return record


tournament_rule_sets_config: "ResourceConfig" = {
    "before_load": [_before_load_tournament_rule_set],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "bannedGroups": make_nested_hints(primary_key=["ruleSetID", "groupID"]),
            "groupPoints": make_nested_hints(primary_key=["ruleSetID", "groupID"]),
            "bannedTypes": make_nested_hints(primary_key=["ruleSetID", "typeID"]),
            "typePoints": make_nested_hints(primary_key=["ruleSetID", "typeID"]),
        },
    },
}
