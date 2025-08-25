from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_school(record: dict[str, Any]) -> dict[str, Any]:
    id_ = record["id"]

    if "startingStations" in record:
        record["startingStations"] = [
            {"schoolID": id_, "stationID": station_id}
            for station_id in record["startingStations"]
        ]

    return record


schools_config: "ResourceConfig" = {
    "before_load": [_before_load_school],
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "startingStations": make_nested_hints(
                primary_key=["schoolID", "stationID"]
            ),
        },
    },
}
