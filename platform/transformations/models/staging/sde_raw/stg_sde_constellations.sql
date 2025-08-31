with
    source as (select * from {{ source("sde_raw", "constellations") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as constellation_uuid,
            constellation_id::bigint as constellation_id,
            faction_id::bigint as faction_id,
            name_id::bigint as name_id,
            region_id::bigint as region_id,
            wormhole_class_id::bigint as wormhole_class_id,

            -- -------- Numerics
            center__x::decimal as center_x,
            center__y::decimal as center_y,
            center__z::decimal as center_z,
            max__x::decimal as maximum_x,
            max__y::decimal as maximum_y,
            max__z::decimal as maximum_z,
            min__x::decimal as minimum_x,
            min__y::decimal as minimum_y,
            min__z::decimal as minimum_z,
            radius::decimal as radius

        from source
    )

select *
from renamed
