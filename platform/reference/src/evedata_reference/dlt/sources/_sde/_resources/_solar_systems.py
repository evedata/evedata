import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from dlt.extract.hints import make_nested_hints

from evedata_reference.dlt.sources._utils import (
    constellation_id_from_solar_system_path,
    inv_names,
    position_dict_from_array,
    region_id_from_solar_system_path,
)

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig


def _before_load_solar_system(record: dict[str, Any]) -> dict[str, Any]:  # noqa: PLR0912, PLR0915
    record["constellationID"] = constellation_id_from_solar_system_path(
        Path(record["_path"])
    )
    record["regionID"] = region_id_from_solar_system_path(Path(record["_path"]))

    names = inv_names(
        Path(record["_path"]).parent.parent.parent.parent.parent.parent
        / "bsd"
        / "invNames.yaml"
    )

    id_ = record["id"]
    record.pop("sunTypeID", None)

    if "center" in record:
        record["center"] = position_dict_from_array(record["center"])
    if "max" in record:
        record["max"] = position_dict_from_array(record["max"])
    if "min" in record:
        record["min"] = position_dict_from_array(record["min"])

    if "secondarySun" in record:
        record["secondarySun"]["id"] = record["secondarySun"].pop("itemID")
        record["secondarySun"]["name"] = names.get(
            record["secondarySun"]["id"], "Name Unknown"
        )
        record["secondarySun"]["position"] = position_dict_from_array(
            record["secondarySun"]["position"]
        )

    if "star" in record:
        record["star"]["name"] = names.get(record["star"]["id"], "Name Unknown")

    if "disallowedAnchorCategories" in record:
        record["disallowedAnchorCategories"] = [
            {"solarSystemID": id_, "categoryID": category_id}
            for category_id in record["disallowedAnchorCategories"]
        ]

    if "disallowedAnchorGroups" in record:
        record["disallowedAnchorGroups"] = [
            {"solarSystemID": id_, "groupID": group_id}
            for group_id in record["disallowedAnchorGroups"]
        ]

    if security := record.get("security"):
        if security >= 0.5:  # noqa: PLR2004
            record["security_status"] = "high"
        elif security > 0.0:
            record["security_status"] = "low"
        elif security <= 0.0:
            record["security_status"] = "null"

    stations: list[dict[str, Any]] = []
    for planet in record.get("planets", []):
        planet["solarSystemID"] = id_
        if "position" in planet:
            planet["position"] = position_dict_from_array(planet["position"])
        planet_id = planet["id"]
        planet["name"] = names.get(planet_id, "Name Unknown")
        for belt in planet.get("asteroidBelts", []):
            belt["solarSystemID"] = id_
            belt["planetID"] = planet_id
            belt["name"] = names.get(belt["id"], "Name Unknown")
            if re.match(r".*\s\d+$", belt["name"]):
                belt["celestial_index"] = int(belt["name"].split()[-1])
            if "position" in belt:
                belt["position"] = position_dict_from_array(belt["position"])
        for moon in planet.get("moons", []):
            moon["solarSystemID"] = id_
            moon["planetID"] = planet_id
            moon["name"] = names.get(moon["id"], "Name Unknown")
            if re.match(r".*\s\d+$", moon["name"]):
                moon["celestial_index"] = int(moon["name"].split()[-1])
            if "position" in moon:
                moon["position"] = position_dict_from_array(moon["position"])
            for station in moon.get("npcStations", []):
                station["solarSystemID"] = id_
                station["planetID"] = planet_id
                station["moonID"] = moon["id"]
                station["name"] = names.get(station["id"], "Name Unknown")
                if "position" in station:
                    station["position"] = position_dict_from_array(station["position"])
            stations.extend(moon.pop("npcStations", []))
        for station in planet.get("npcStations", []):
            station["solarSystemID"] = id_
            station["planetID"] = planet_id
            station["name"] = names.get(station["id"], "Name Unknown")
            if "position" in station:
                station["position"] = position_dict_from_array(station["position"])
        stations.extend(planet.pop("npcStations", []))
        record["stations"] = stations

    for stargate in record.get("stargates", []):
        stargate["solarSystemID"] = id_
        stargate["name"] = names.get(stargate["id"], "Name Unknown")
        stargate["destinationID"] = stargate.pop("destination")
        if "position" in stargate:
            stargate["position"] = position_dict_from_array(stargate["position"])
    return record


solar_systems_config: "ResourceConfig" = {
    "rename_columns": {"solarSystemID": "id"},
    "before_load": [_before_load_solar_system],
    "name_from_inv_names": True,
    "hints": {
        "primary_key": "id",
        "nested_hints": {
            "disallowedAnchorCategories": make_nested_hints(
                primary_key=["solarSystemID", "categoryID"]
            ),
            "disallowedAnchorGroups": make_nested_hints(
                primary_key=["solarSystemID", "groupID"]
            ),
            "planets": make_nested_hints(primary_key=["id"]),
            ("planets", "moons"): make_nested_hints(primary_key=["id"]),
            ("planets", "asteroidBelts"): make_nested_hints(primary_key=["id"]),
            "stations": make_nested_hints(primary_key=["id"]),
            "stargates": make_nested_hints(primary_key=["id"]),
        },
    },
}
