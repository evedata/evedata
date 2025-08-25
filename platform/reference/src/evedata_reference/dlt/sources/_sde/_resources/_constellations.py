from pathlib import Path
from typing import TYPE_CHECKING, Any

from evedata_reference.dlt.sources._utils import (
    position_dict_from_array,
    region_id_from_constellation_path,
)

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_constellation(record: dict[str, Any]) -> dict[str, Any]:
    record["regionID"] = region_id_from_constellation_path(Path(record["_path"]))

    if "center" in record:
        record["center"] = position_dict_from_array(record["center"])
    if "max" in record:
        record["max"] = position_dict_from_array(record["max"])
    if "min" in record:
        record["min"] = position_dict_from_array(record["min"])

    return record


constellations_config: "ResourceConfig" = {
    "rename_columns": {"constellationID": "id"},
    "before_load": [_before_load_constellation],
    "name_from_inv_names": True,
    "hints": {"primary_key": "id"},
}
