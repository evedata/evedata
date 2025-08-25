from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_mutaplasmid(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    for attribute in record.get("attributeIDs", []):
        attribute["mutaplasmidID"] = id_
        attribute["dogmaAttributeID"] = attribute.pop("id")
    record["attributes"] = record.pop("attributeIDs", None)

    mappings: list[dict[str, Any]] = []
    for mapping in record.get("inputOutputMapping", []):
        mappings.extend(
            [
                {"mutaplasmidID": id_, "inputTypeID": type_, "outputTypeID": mapping["resultingType"]}
                for type_ in mapping["applicableTypes"]
            ]
        )
    record.pop("inputOutputMapping", None)
    record["mappings"] = mappings

    return record


mutaplasmids_config: "ResourceConfig" = {
    "before_load": [_before_load_mutaplasmid],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "attributes": {"primary_key": ["mutaplasmidID", "dogmaAttributeID"]},
            "mappings": {"primary_key": ["mutaplasmidID", "inputTypeID", "outputTypeID"]},
        },
    },
}
