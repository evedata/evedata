with
    source as (select * from {{ source("hde_raw", "dogma_effect_categories") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as effect_category_uuid,
            key::bigint as effect_category_id,

            -- -------- Text
            value::text as name

        from source
    )

select *
from renamed
