from pathlib import Path
from typing import TYPE_CHECKING, Any

from evedata_platform_extractors._utils._sources import (
    position_dict_from_array,
)

if TYPE_CHECKING:
    from evedata_platform_extractors._types import ResourceConfig


def _before_load_region(record: dict[str, Any]) -> dict[str, Any]:
    base_path = Path(record.pop("_dlt_base_path"))
    resource_path = base_path / Path(record["_dlt_resource_path"])
    record["universe"] = str(Path(resource_path.parent.parent.stem))
    if "center" in record:
        record["center"] = position_dict_from_array(record["center"])
    if "max" in record:
        record["max"] = position_dict_from_array(record["max"])
    if "min" in record:
        record["min"] = position_dict_from_array(record["min"])
    return record


regions_config: "ResourceConfig" = {
    "before_load": [_before_load_region],
}
