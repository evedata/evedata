from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_planet_schematic(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    record["pins"] = [{"schematicID": id_, "typeID": pin} for pin in record["pins"]]

    types = record.pop("types", [])
    inputs: list[dict[str, Any]] = []
    outputs: list[dict[str, Any]] = []
    for type_ in types:
        if type_.get("isInput"):
            inputs.append(
                {
                    "schematicID": id_,
                    "typeID": type_["id"],
                    "quantity": type_["quantity"],
                }
            )
        else:
            outputs.append(
                {
                    "schematicID": id_,
                    "typeID": type_["id"],
                    "quantity": type_["quantity"],
                }
            )
    record["inputs"] = inputs
    record["outputs"] = outputs
    return record


planet_schematics_config: "ResourceConfig" = {
    "before_load": [_before_load_planet_schematic],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "pins": make_nested_hints(primary_key=["schematicID", "typeID"]),
            "inputs": make_nested_hints(primary_key=["schematicID", "typeID"]),
            "outputs": make_nested_hints(primary_key=["schematicID", "typeID"]),
        },
    },
}
