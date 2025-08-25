from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_skin(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]
    del record["skinID"]
    record["types"] = [
        {"skinID": id_, "typeID": type_id} for type_id in record.get("types", [])
    ]
    return record


skins_config: "ResourceConfig" = {
    "before_load": [_before_load_skin],
    "hints": {
        "primary_key": "id",
        "nested_hints": {"types": make_nested_hints(primary_key=["skinID", "typeID"])},
    },
}
