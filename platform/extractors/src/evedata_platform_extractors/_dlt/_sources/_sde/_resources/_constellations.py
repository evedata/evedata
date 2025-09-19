from pathlib import Path
from typing import TYPE_CHECKING, Any

from evedata_platform_extractors._utils._sources import (
    position_dict_from_array,
    region_id_from_constellation_path,
)

if TYPE_CHECKING:
    from evedata_platform_extractors._types import ResourceConfig


def _before_load_constellation(record: dict[str, Any]) -> dict[str, Any]:
    base_path = Path(record.pop("_dlt_base_path"))
    resource_path = base_path / Path(record["_dlt_resource_path"])
    record["regionID"] = region_id_from_constellation_path(resource_path)

    if "center" in record:
        record["center"] = position_dict_from_array(record["center"])
    if "max" in record:
        record["max"] = position_dict_from_array(record["max"])
    if "min" in record:
        record["min"] = position_dict_from_array(record["min"])

    return record


constellations_config: "ResourceConfig" = {
    "before_load": [_before_load_constellation],
}
