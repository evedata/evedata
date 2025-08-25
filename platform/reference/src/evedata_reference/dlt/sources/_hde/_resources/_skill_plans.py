from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_skill_plan(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    for milestone in record.get("milestones", []):
        milestone["skillPlanID"] = id_

    for requirement in record.get("skillRequirements", []):
        requirement["skillPlanID"] = id_

    return record


skill_plans_config: "ResourceConfig" = {
    "before_load": [_before_load_skill_plan],
    "rename_columns": {
        "npcCorporationDivision": "npcCorporationDivisionID",
    },
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "milestones": make_nested_hints(primary_key=["skillPlanID", "typeID"]),
            "skillRequirements": make_nested_hints(primary_key=["skillPlanID", "typeID"]),
        },
    },
}
