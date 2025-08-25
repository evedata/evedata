from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_industry_installation_type(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    for assembly_line in record.get("assembly_lines", []):
        assembly_line["installationTypeID"] = id_
        assembly_line["assemblyLineID"] = assembly_line.pop("assemblyLine")

    return record


industry_installation_types_config: "ResourceConfig" = {
    "before_load": [_before_load_industry_installation_type],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "assembly_lines": make_nested_hints(
                primary_key=["installationTypeID", "assemblyLineID"]
            ),
        },
    },
}
