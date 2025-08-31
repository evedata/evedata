with
    source as (select * from {{ source("sde_raw", "dogma_attribute_categories") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as attribute_category_uuid,
            id::bigint as attribute_category_id,

            -- -------- Text
            description::text as description,
            name::text as name

        from source
    )

select *
from renamed
