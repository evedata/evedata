with
    source as (select * from {{ source("sde_raw", "type_dogma__dogma_effects") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_effect_uuid,
            _dlt_parent_id::text as type_dogma_uuid,
            effect_id::bigint as effect_id,

            -- -------- Booleans
            is_default::boolean as is_default

        from source
    )

select *
from renamed
