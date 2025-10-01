{{ config(materialized="table") }}

with
    moon_stations as (select * from {{ ref("stg_sde_moon_stations") }}),

    moons as (select * from {{ ref("stg_sde_moons") }}),

    planet_stations as (select * from {{ ref("stg_sde_planet_stations") }}),

    planets as (select * from {{ ref("stg_sde_planets") }}),

    systems as (select * from {{ ref("stg_sde_systems") }}),

    systems_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from systems
        window w as (partition by system_id order by sde_version)
    ),

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
            reprocessing_stations_take,
            sde_version
        from {{ ref("stg_sde_stations") }}
    ),

    stations_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from stations
        window w as (partition by station_id order by sde_version)
    ),

    planet_stations_scd2 as (
        select
            planet_stations.*,
            systems.sde_version as from_sde_version,
            lead(systems.sde_version) over w as to_sde_version
        from planet_stations
        inner join planets on planet_stations.planet_uuid = planets.planet_uuid
        inner join systems_scd2 as systems on planets.system_uuid = systems.system_uuid
        window w as (partition by station_id order by sde_version)
    ),

    moon_stations_scd2 as (
        select
            moon_stations.*,
            systems.sde_version as from_sde_version,
            lead(systems.sde_version) over w as to_sde_version
        from moon_stations
        inner join moons on moon_stations.moon_uuid = moons.moon_uuid
        inner join planets on moons.planet_uuid = planets.planet_uuid
        inner join systems_scd2 as systems on planets.system_uuid = systems.system_uuid
        window w as (partition by station_id order by sde_version)
    ),

    joined as (
        select stations.*, planets.planet_id, moons.moon_id
        from stations_scd2 as stations
        left join moon_stations_scd2 as moon_stations on stations.station_id = moon_stations.station_id and stations.from_sde_version = moon_stations.from_sde_version
        left join moons on moon_stations.moon_uuid = moons.moon_uuid
        left join planet_stations_scd2 as planet_stations on stations.station_id = planet_stations.station_id and stations.from_sde_version = planet_stations.from_sde_version
        left join planets on planet_stations.planet_uuid = planets.planet_uuid
    ),

    final as (
        select
            *,

            {{ dbt_utils.generate_surrogate_key(["station_id", "from_sde_version"]) }}
            as station_sk,
            coalesce(to_sde_version is null, false) as is_current
        from joined
    )

select *
from final
