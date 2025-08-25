from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_blueprint(record: dict[str, Any]) -> dict[str, Any]:  # noqa: PLR0912
    blueprint_id = record["id"]
    if "copying" in record["activities"]:
        if "materials" in record["activities"]["copying"]:
            for material in record["activities"]["copying"]["materials"]:
                material["blueprintID"] = blueprint_id
        if "skills" in record["activities"]["copying"]:
            for skill in record["activities"]["copying"]["skills"]:
                skill["blueprintID"] = blueprint_id
    if "invention" in record["activities"]:
        if "materials" in record["activities"]["invention"]:
            for material in record["activities"]["invention"]["materials"]:
                material["blueprintID"] = blueprint_id
        if "products" in record["activities"]["invention"]:
            for product in record["activities"]["invention"]["products"]:
                product["blueprintID"] = blueprint_id
        if "skills" in record["activities"]["invention"]:
            for skill in record["activities"]["invention"]["skills"]:
                skill["blueprintID"] = blueprint_id
    if "manufacturing" in record["activities"]:
        if "materials" in record["activities"]["manufacturing"]:
            for material in record["activities"]["manufacturing"]["materials"]:
                material["blueprintID"] = blueprint_id
        if "products" in record["activities"]["manufacturing"]:
            for product in record["activities"]["manufacturing"]["products"]:
                product["blueprintID"] = blueprint_id
        if "skills" in record["activities"]["manufacturing"]:
            for skill in record["activities"]["manufacturing"]["skills"]:
                skill["blueprintID"] = blueprint_id
    if "reaction" in record["activities"]:
        if "materials" in record["activities"]["reaction"]:
            for material in record["activities"]["reaction"]["materials"]:
                material["blueprintID"] = blueprint_id
        if "products" in record["activities"]["reaction"]:
            for product in record["activities"]["reaction"]["products"]:
                product["blueprintID"] = blueprint_id
        if "skills" in record["activities"]["reaction"]:
            for skill in record["activities"]["reaction"]["skills"]:
                skill["blueprintID"] = blueprint_id
    if "research_material" in record["activities"]:
        if "materials" in record["activities"]["research_material"]:
            for material in record["activities"]["research_material"]["materials"]:
                material["blueprintID"] = blueprint_id
        if "skills" in record["activities"]["research_material"]:
            for skill in record["activities"]["research_material"]["skills"]:
                skill["blueprintID"] = blueprint_id
    if "research_time" in record["activities"]:
        if "materials" in record["activities"]["research_time"]:
            for material in record["activities"]["research_time"]["materials"]:
                material["blueprintID"] = blueprint_id
        if "skills" in record["activities"]["research_time"]:
            for skill in record["activities"]["research_time"]["skills"]:
                skill["blueprintID"] = blueprint_id
    return record


blueprints_config: "ResourceConfig" = {
    "before_load": [_before_load_blueprint],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            ("activities", "copying", "materials"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "copying", "skills"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "invention", "materials"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "invention", "products"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "invention", "skills"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "manufacturing", "materials"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "manufacturing", "products"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "manufacturing", "skills"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "reaction", "materials"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "reaction", "products"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "reaction", "skills"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "research_material", "materials"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "research_material", "skills"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "research_time", "materials"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
            ("activities", "research_time", "skills"): make_nested_hints(
                primary_key=["blueprintID", "typeID"]
            ),
        },
    },
}
