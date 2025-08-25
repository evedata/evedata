from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_industry_assembly_line(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    for category in record.get("details_per_category", []):
        category["assemblyLineID"] = id_
    record["categories"] = record.pop("details_per_category", [])

    for group in record.get("details_per_group", []):
        group["assemblyLineID"] = id_
    record["groups"] = record.pop("details_per_group", [])

    for type_list in record.get("details_per_type_list", []):
        type_list["assemblyLineID"] = id_
    record["typeLists"] = record.pop("details_per_type_list", [])

    return record


industry_assembly_lines_config: "ResourceConfig" = {
    "before_load": [_before_load_industry_assembly_line],
    "rename_columns": {"activity": "activityID"},
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "categories": make_nested_hints(
                primary_key=["assemblyLineID", "categoryID"]
            ),
            "groups": make_nested_hints(primary_key=["assemblyLineID", "groupID"]),
            "typeLists": make_nested_hints(
                primary_key=["assemblyLineID", "typeListID"]
            ),
        },
    },
}
