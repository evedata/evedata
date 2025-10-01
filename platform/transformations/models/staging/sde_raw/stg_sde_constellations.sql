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

            -- -------- Text
            sde_version::text as sde_version,

            -- -------- Numerics
            center__x::double as center_x,
            center__y::double as center_y,
            center__z::double as center_z,
            max__x::double as maximum_x,
            max__y::double as maximum_y,
            max__z::double as maximum_z,
            min__x::double as minimum_x,
            min__y::double as minimum_y,
            min__z::double as minimum_z,
            radius::decimal as radius

        from source
    )

select *
from renamed
