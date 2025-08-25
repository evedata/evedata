from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_certificate(record: dict[str, Any]) -> dict[str, Any]:
    certificate_id = record["id"]
    if "recommendedFor" in record:
        new_recommended_for = [
            {"certificateID": certificate_id, "typeID": entry}
            for entry in record["recommendedFor"]
        ]
        record["recommendedFor"] = new_recommended_for
    if "skillTypes" in record:
        new_skill_types = [
            {
                "certificateID": certificate_id,
                "typeID": entry["id"],
                "advanced": entry["advanced"],
                "basic": entry["basic"],
                "elite": entry["elite"],
                "improved": entry["improved"],
                "standard": entry["standard"],
            }
            for entry in record["skillTypes"]
        ]
        record["skillTypes"] = new_skill_types
    return record


certificates_config: "ResourceConfig" = {
    "before_load": [_before_load_certificate],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "recommendedFor": make_nested_hints(
                primary_key=["certificateID", "typeID"]
            ),
            "skillTypes": make_nested_hints(primary_key=["certificateID", "typeID"]),
        },
    },
}
