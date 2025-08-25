from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_industry_target_filter(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    if "categoryIDs" in record:
        record["categories"] = [
            {"targetFilterID": id_, "categoryID": category_id}
            for category_id in record["categoryIDs"]
        ]
        record.pop("categoryIDs", None)

    if "groupIDs" in record:
        record["groups"] = [
            {"targetFilterID": id_, "groupID": group_id}
            for group_id in record["groupIDs"]
        ]
        record.pop("groupIDs", None)

    return record


industry_target_filters_config: "ResourceConfig" = {
    "before_load": [_before_load_industry_target_filter],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "categories": make_nested_hints(
                primary_key=["targetFilterID", "categoryID"]
            ),
            "groups": make_nested_hints(primary_key=["targetFilterID", "groupID"]),
        },
    },
}
