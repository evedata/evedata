with
    source as (
        select * from {{ source("sde_raw", "solar_systems__planets__npc_stations") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as planet_station_uuid,
            _dlt_parent_id::text as planet_uuid,
            id::bigint as station_id,
            graphic_id::bigint as graphic_id,
            owner_id::bigint as npc_corporation_id,
            reprocessing_hangar_flag::bigint as reprocessing_hangar_flag_id,
            operation_id::bigint as station_operation_id,
            type_id::bigint as station_type_id,

            -- -------- Numerics
            position__x::decimal as position_x,
            position__y::decimal as position_y,
            position__z::decimal as position_z,
            reprocessing_efficiency::decimal as reprocessing_efficiency,
            reprocessing_stations_take::decimal as reprocessing_stations_take,

            -- -------- Booleans
            is_conquerable::boolean as is_conquerable,
            use_operation_name::boolean as uses_operation_name

        from source
    )

select *
from renamed
