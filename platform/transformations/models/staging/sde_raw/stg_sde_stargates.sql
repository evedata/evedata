with
    source as (select * from {{ source("sde_raw", "solar_systems__stargates") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as stargate_uuid,
            _dlt_parent_id::text as system_uuid,
            id::bigint as stargate_id,
            destination::bigint as destination_stargate_id,
            type_id::bigint as type_id,

            -- -------- Numerics
            position__x::decimal as position_x,
            position__y::decimal as position_y,
            position__z::decimal as position_z

        from source
    )

select *
from renamed
