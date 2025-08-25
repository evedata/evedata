from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_research_agent(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]
    for skill in record.get("skills", []):
        skill["researchAgentID"] = id_
    return record


research_agents_config: "ResourceConfig" = {
    "before_load": [_before_load_research_agent],
    "hints": {
        "primary_key": "id",
        "nested_hints": {"skills": make_nested_hints(primary_key=["researchAgentID", "typeID"])},
    },
}
