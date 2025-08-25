from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_type_material(record: dict[str, Any]) -> dict[str, Any]:
    for material in record.get("materials", []):
        material["typeID"] = record["id"]

    record["types"] = record.pop("materials", [])

    return record


type_materials_config: "ResourceConfig" = {
    "before_load": [_before_load_type_material],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "types": make_nested_hints(primary_key=["typeID", "materialTypeID"]),
        },
    },
}
