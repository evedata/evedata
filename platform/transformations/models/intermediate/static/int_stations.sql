with
    moon_stations as (select * from {{ ref("stg_sde_moon_stations") }}),
    moons as (select * from {{ ref("stg_sde_moons") }}),
    planet_stations as (select * from {{ ref("stg_sde_planet_stations") }}),
    planets as (select * from {{ ref("stg_sde_planets") }}),

    stations as (
        select
            station_id,
            npc_corporation_id,
            reprocessing_hangar_flag_id,
            system_id,
            type_id,
            name,
            docking_cost_per_volume,
            max_dockable_volume,
            office_rental_cost,
            position_x,
            position_y,
            position_z,
            reprocessing_efficiency,
            reprocessing_stations_take
        from {{ ref("stg_sde_stations") }}
    ),

    joined as (
        select stations.*, planets.planet_id, moons.moon_id
        from stations
        left join moon_stations on stations.station_id = moon_stations.station_id
        left join moons on moon_stations.moon_uuid = moons.moon_uuid
        left join planet_stations on stations.station_id = planet_stations.station_id
        left join planets on planet_stations.planet_uuid = planets.planet_uuid
    )

select *
from joined
