with
    source as (select * from {{ source("raw_sde", "npc_stations") }}),

    renamed as (

        select
            _key as npc_station_id,
            celestial_index,
            operation_id,
            orbit_id,
            orbit_index,
            owner_id,
            position__x,
            position__y,
            position__z,
            reprocessing_efficiency,
            reprocessing_hangar_flag,
            reprocessing_stations_take,
            solar_system_id,
            type_id,
            use_operation_name,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
