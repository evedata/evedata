from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_control_tower_resource(record: dict[str, Any]) -> dict[str, Any]:
    type_id = record.get("id")

    resources: list[dict[str, Any]] = record.get("resources", [])
    for resource in resources:
        resource["controlTowerTypeID"] = type_id

    return record


control_tower_resources_config: "ResourceConfig" = {
    "before_load": [_before_load_control_tower_resource],
    "hints": {
        "primary_key": "id",
        "nested_hints": {"resources": {"primary_key": ["controlTowerTypeID", "resourceTypeID"]}},
    },
}
