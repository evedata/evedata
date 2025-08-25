from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_race(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]
    for skill in record.get("skills", []):
        skill["raceID"] = id_
        skill["typeID"] = skill.pop("id")
        skill["level"] = skill.pop("value")
    return record


races_config: "ResourceConfig" = {
    "before_load": [_before_load_race],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "skills": make_nested_hints(primary_key=["raceID", "typeID"]),
        },
    },
}
