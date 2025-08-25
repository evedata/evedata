from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_station_operation(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    for station_type in record.get("stationTypes", []):
        station_type["operationID"] = id_
        station_type["raceID"] = station_type.pop("id")
        station_type["typeID"] = station_type.pop("value")

    record["services"] = [{"operationID": id_, "serviceID": service_id} for service_id in record.get("services", [])]

    return record


station_operations_config: "ResourceConfig" = {
    "before_load": [_before_load_station_operation],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "services": make_nested_hints(primary_key=["operationID", "serviceID"]),
            "stationTypes": make_nested_hints(primary_key=["operationID", "raceID"]),
        },
    },
}
