from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _preprocess_type_dogma(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    for dogma_attribute in record.get("dogmaAttributes", []):
        dogma_attribute["type_id"] = id_

    for dogma_effect in record.get("dogmaEffects", []):
        dogma_effect["type_id"] = id_

    record["attributes"] = record.pop("dogmaAttributes", [])
    record["effects"] = record.pop("dogmaEffects", [])

    return record


type_dogma_config: "ResourceConfig" = {
    "before_load": [_preprocess_type_dogma],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "attributes": make_nested_hints(primary_key=["type_id", "attribute_id"]),
            "effects": make_nested_hints(primary_key=["type_id", "effect_id"]),
        },
    },
}
