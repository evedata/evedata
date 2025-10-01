from pathlib import Path
from typing import TYPE_CHECKING, Any

from evedata_platform_extract._utils._sources import (
    constellation_id_from_solar_system_path,
    position_dict_from_array,
)

if TYPE_CHECKING:
    from evedata_platform_extract._types import ResourceConfig


def _before_load_solar_system(record: dict[str, Any]) -> dict[str, Any]:  # noqa: PLR0912
    base_path = Path(record.pop("_dlt_base_path"))
    resource_path = base_path / Path(record["_dlt_resource_path"])

    record["constellationID"] = constellation_id_from_solar_system_path(resource_path)

    if "center" in record:
        record["center"] = position_dict_from_array(record["center"])
    if "max" in record:
        record["max"] = position_dict_from_array(record["max"])
    if "min" in record:
        record["min"] = position_dict_from_array(record["min"])

    if "secondarySun" in record:
        record["secondarySun"]["position"] = position_dict_from_array(
            record["secondarySun"]["position"]
        )

    for planet in record.get("planets", []):
        if "position" in planet:
            planet["position"] = position_dict_from_array(planet["position"])
        for index, belt in enumerate(planet.get("asteroidBelts", [])):
            belt["celestialIndex"] = index
            if "position" in belt:
                belt["position"] = position_dict_from_array(belt["position"])
        for index, moon in enumerate(planet.get("moons", [])):
            moon["celestialIndex"] = index
            if "position" in moon:
                moon["position"] = position_dict_from_array(moon["position"])
            for station in moon.get("npcStations", []):
                if "position" in station:
                    station["position"] = position_dict_from_array(station["position"])
        for station in planet.get("npcStations", []):
            if "position" in station:
                station["position"] = position_dict_from_array(station["position"])

    for stargate in record.get("stargates", []):
        if "position" in stargate:
            stargate["position"] = position_dict_from_array(stargate["position"])
    return record


solar_systems_config: "ResourceConfig" = {
    "before_load": [_before_load_solar_system],
}
