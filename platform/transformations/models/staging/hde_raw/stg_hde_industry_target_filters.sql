with
    source as (select * from {{ source("hde_raw", "industry_target_filters") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_target_filter_uuid,
            id::bigint as industry_target_filter_id,

            -- -------- Text
            name::text as name

        from source
    )

select *
from renamed
