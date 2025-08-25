from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_type(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    if "masteries" in record:
        new_masteries: list[dict[str, Any]] = []
        for mastery in record["masteries"]:
            new_masteries.extend(
                [
                    {"typeID": id_, "certificateID": certificate_id, "level": mastery["id"]}
                    for certificate_id in mastery.get("value", [])
                ]
            )
        record["masteries"] = new_masteries

    if "traits" in record:
        for index, trait in enumerate(record["traits"].get("miscBonuses", [])):
            trait["typeID"] = id_
            trait["traitIndex"] = index

        for index, trait in enumerate(record["traits"].get("roleBonuses", [])):
            trait["typeID"] = id_
            trait["traitIndex"] = index

        new_trait_types: list[dict[str, Any]] = []
        for trait_type in record["traits"].get("types", []):
            for index, bonus in enumerate(trait_type["value"]):
                trait = {
                    "typeID": id_,
                    **bonus,
                    "traitIndex": index,
                }
                trait["traitTypeID"] = trait_type["id"]
                new_trait_types.append(trait)
        record["traits"].pop("types", None)
        record["traits"]["typeBonuses"] = new_trait_types

    return record


types_config: "ResourceConfig" = {
    "before_load": [_before_load_type],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "masteries": make_nested_hints(primary_key=["typeID", "certificateID"]),
            ("traits", "miscBonuses"): make_nested_hints(primary_key=["typeID", "traitIndex"]),
            ("traits", "roleBonuses"): make_nested_hints(primary_key=["typeID", "traitIndex"]),
            ("traits", "typeBonuses"): make_nested_hints(primary_key=["typeID", "traitTypeID", "traitIndex"]),
        },
    },
}
