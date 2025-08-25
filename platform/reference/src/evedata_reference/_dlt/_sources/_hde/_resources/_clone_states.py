from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_clone_state(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    if "skills" in record:
        record["skills"] = [
            {"cloneStateID": id_, "typeID": skill["id"], "level": skill["value"]}
            for skill in record["skills"]
        ]

    return record


clone_states_config: "ResourceConfig" = {
    "before_load": [_before_load_clone_state],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "skills": {"primary_key": ["cloneStateID", "typeID"]},
        },
    },
}
