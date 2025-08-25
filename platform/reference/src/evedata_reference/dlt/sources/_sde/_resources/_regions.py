from pathlib import Path
from typing import TYPE_CHECKING, Any

from evedata_reference.dlt.sources._utils import (
    position_dict_from_array,
)

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_region(record: dict[str, Any]) -> dict[str, Any]:
    record["universe"] = str(Path(record["_path"]).parent.parent.stem)
    if "center" in record:
        record["center"] = position_dict_from_array(record["center"])
    if "max" in record:
        record["max"] = position_dict_from_array(record["max"])
    if "min" in record:
        record["min"] = position_dict_from_array(record["min"])
    return record


regions_config: "ResourceConfig" = {
    "rename_columns": {"nebula": "nebula_id", "regionID": "id"},
    "before_load": [_before_load_region],
    "name_from_inv_names": True,
    "hints": {"primary_key": "id"},
}
