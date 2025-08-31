with
    source as (select * from {{ source("sde_raw", "type_dogma__dogma_attributes") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_attribute_uuid,
            _dlt_parent_id::text as type_dogma_uuid,
            attribute_id::bigint as attribute_id,

            -- -------- Numerics
            value::decimal as value

        from source
    )

select *
from renamed
