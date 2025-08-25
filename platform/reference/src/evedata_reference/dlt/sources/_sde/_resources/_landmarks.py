from typing import TYPE_CHECKING, Any

from evedata_reference.dlt.sources._utils import (
    position_dict_from_array,
)

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_landmark(record: dict[str, Any]) -> dict[str, Any]:
    if "position" in record:
        record["position"] = position_dict_from_array(record["position"])
    return record


landmarks_config: "ResourceConfig" = {
    "before_load": [_before_load_landmark],
    "hints": {"primary_key": "id"},
}
