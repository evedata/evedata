with
    source as (select * from {{ source("sde_raw", "inv_positions") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as item_position_uuid,
            item_id::bigint as item_id,

            -- -------- Text
            sde_version::text as sde_version,

            -- -------- Numerics
            pitch::decimal as pitch,
            roll::decimal as roll,
            x::decimal as x,
            y::decimal as y,
            yaw::decimal as yaw,
            z::decimal as z

        from source
    )

select *
from renamed
