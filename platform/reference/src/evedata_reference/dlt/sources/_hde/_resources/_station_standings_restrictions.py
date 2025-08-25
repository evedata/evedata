from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_station_standings_restriction(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    for service in record.get("services", []):
        service["stationID"] = id_
        service["serviceID"] = service.pop("id")
        service["standing"] = service.pop("value")

    return record


station_standings_restrictions_config: "ResourceConfig" = {
    "before_load": [_before_load_station_standings_restriction],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "services": make_nested_hints(primary_key=["stationID", "serviceID"]),
        },
    },
}
