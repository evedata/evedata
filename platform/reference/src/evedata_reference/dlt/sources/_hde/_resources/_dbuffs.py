from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_dbuff(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    for modifier in record.get("itemModifiers", []):
        modifier["dbuff_id"] = id_

    for modifier in record.get("locationModifiers", []):
        modifier["dbuff_id"] = id_

    for modifier in record.get("locationGroupModifiers", []):
        modifier["dbuff_id"] = id_

    for modifier in record.get("locationRequiredSkillModifiers", []):
        modifier["dbuff_id"] = id_

    return record


dbuffs_config: "ResourceConfig" = {
    "before_load": [_before_load_dbuff],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "itemModifiers": {"primary_key": ["dbuff_id", "dogmaAttributeID"]},
            "locationModifiers": {"primary_key": ["dbuff_id", "dogmaAttributeID"]},
            "locationGroupModifiers": {
                "primary_key": ["dbuff_id", "dogmaAttributeID", "groupID"]
            },
            "locationRequiredSkillModifiers": {
                "primary_key": ["dbuff_id", "dogmaAttributeID", "skillID"]
            },
        },
    },
}
