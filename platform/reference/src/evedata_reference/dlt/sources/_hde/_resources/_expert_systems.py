from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_expert_system(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    if "associatedShipTypes" in record:
        record["associatedShipTypes"] = [
            {"expertSystemID": id_, "typeID": type_id} for type_id in record["associatedShipTypes"]
        ]
        record["shipTypes"] = record.pop("associatedShipTypes")

    for skill in record.get("skillsGranted", []):
        skill["expertSystemID"] = id_
        skill["typeID"] = skill.pop("id")
        skill["level"] = skill.pop("value")

    return record


expert_systems_config: "ResourceConfig" = {
    "before_load": [_before_load_expert_system],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "shipTypes": make_nested_hints(primary_key=["expertSystemID", "typeID"]),
            "skillsGranted": make_nested_hints(primary_key=["expertSystemID", "typeID"]),
        },
    },
}
