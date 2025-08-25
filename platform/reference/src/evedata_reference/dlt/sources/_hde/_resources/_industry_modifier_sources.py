from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_industry_modifier_source(record: dict[str, Any]) -> dict[str, Any]:  # noqa: PLR0912
    id_ = record["id"]

    if "copying" in record and "cost" in record["copying"]:
        for source in record["copying"]["cost"]:
            source["modifierSourceID"] = id_

    if "copying" in record and "time" in record["copying"]:
        for source in record["copying"]["time"]:
            source["modifierSourceID"] = id_

    if "invention" in record and "cost" in record["invention"]:
        for source in record["invention"]["cost"]:
            source["modifierSourceID"] = id_

    if "invention" in record and "time" in record["invention"]:
        for source in record["invention"]["time"]:
            source["modifierSourceID"] = id_

    if "manufacturing" in record and "cost" in record["manufacturing"]:
        for source in record["manufacturing"]["cost"]:
            source["modifierSourceID"] = id_

    if "manufacturing" in record and "material" in record["manufacturing"]:
        for source in record["manufacturing"]["material"]:
            source["modifierSourceID"] = id_

    if "manufacturing" in record and "time" in record["manufacturing"]:
        for source in record["manufacturing"]["time"]:
            source["modifierSourceID"] = id_

    if "reaction" in record and "cost" in record["reaction"]:
        for source in record["reaction"]["cost"]:
            source["modifierSourceID"] = id_

    if "reaction" in record and "material" in record["reaction"]:
        for source in record["reaction"]["material"]:
            source["modifierSourceID"] = id_

    if "reaction" in record and "time" in record["reaction"]:
        for source in record["reaction"]["time"]:
            source["modifierSourceID"] = id_

    if "research_material" in record and "cost" in record["research_material"]:
        for source in record["research_material"]["cost"]:
            source["modifierSourceID"] = id_

    if "research_material" in record and "time" in record["research_material"]:
        for source in record["research_material"]["time"]:
            source["modifierSourceID"] = id_

    if "research_time" in record and "cost" in record["research_time"]:
        for source in record["research_time"]["cost"]:
            source["modifierSourceID"] = id_

    if "research_time" in record and "time" in record["research_time"]:
        for source in record["research_time"]["time"]:
            source["modifierSourceID"] = id_

    return record


industry_modifier_sources_config: "ResourceConfig" = {
    "before_load": [_before_load_industry_modifier_source],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            ("copying", "cost"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("copying", "time"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("invention", "cost"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("invention", "time"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("manufacturing", "cost"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("manufacturing", "material"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("manufacturing", "time"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("reaction", "cost"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("reaction", "material"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("reaction", "time"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("research_material", "cost"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("research_material", "time"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("research_time", "cost"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
            ("research_time", "time"): make_nested_hints(
                primary_key=["modifierSourceID", "dogmaAttributeID"]
            ),
        },
    },
}
