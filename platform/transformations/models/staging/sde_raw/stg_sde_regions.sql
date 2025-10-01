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
            sde_version::text as sde_version,
            universe::text as universe_name,

            -- -------- Numerics
            center__x::double as center_x,
            center__y::double as center_y,
            center__z::double as center_z,
            max__x::double as maximum_x,
            max__y::double as maximum_y,
            max__z::double as maximum_z,
            min__x::double as minimum_x,
            min__y::double as minimum_y,
            min__z::double as minimum_z

        from source
    )

select *
from renamed
