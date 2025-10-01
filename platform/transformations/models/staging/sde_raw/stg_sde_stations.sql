with
    source as (select * from {{ source("sde_raw", "stations") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as station_uuid,
            station_id::bigint as station_id,
            constellation_id::bigint as constellation_id,
            corporation_id::bigint as npc_corporation_id,
            operation_id::bigint as station_operation_id,
            region_id::bigint as region_id,
            reprocessing_hangar_flag::bigint as reprocessing_hangar_flag_id,
            solar_system_id::bigint as system_id,
            station_type_id::bigint as type_id,

            -- -------- Text
            station_name::text as name,
            sde_version::text as sde_version,

            -- -------- Numerics
            docking_cost_per_volume::bigint as docking_cost_per_volume,
            max_ship_volume_dockable::bigint as max_dockable_volume,
            office_rental_cost::bigint as office_rental_cost,
            x::double as position_x,
            y::double as position_y,
            z::double as position_z,
            reprocessing_efficiency::decimal as reprocessing_efficiency,
            reprocessing_stations_take::decimal as reprocessing_stations_take,
            security::decimal as security

        from source
    )

select *
from renamed
