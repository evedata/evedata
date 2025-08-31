with
    source as (select * from {{ source("sde_raw", "regions") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as region_uuid,
            region_id::bigint as region_id,
            description_id::bigint as description_id,
            faction_id::bigint as faction_id,
            name_id::bigint as name_id,
            nebula::bigint as nebula_id,
            wormhole_class_id::bigint as wormhole_class_id,

            -- -------- Text
            universe::text as universe_name,

            -- -------- Numerics
            center__x::decimal as center_x,
            center__y::decimal as center_y,
            center__z::decimal as center_z,
            max__x::decimal as maximum_x,
            max__y::decimal as maximum_y,
            max__z::decimal as maximum_z,
            min__x::decimal as minimum_x,
            min__y::decimal as minimum_y,
            min__z::decimal as minimum_z

        from source
    )

select *
from renamed
