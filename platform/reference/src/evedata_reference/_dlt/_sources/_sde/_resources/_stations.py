from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from evedata_reference._types import ResourceConfig


def _before_load_station(record: dict[str, Any]) -> dict[str, Any]:
    position = {
        "x": record.pop("x"),
        "y": record.pop("y"),
        "z": record.pop("z"),
    }
    record["position"] = position

    return record


stations_config: "ResourceConfig" = {
    "before_load": [_before_load_station],
    "rename_columns": {"stationID": "id", "stationName": "name"},
    "hints": {"primary_key": "id"},
}
