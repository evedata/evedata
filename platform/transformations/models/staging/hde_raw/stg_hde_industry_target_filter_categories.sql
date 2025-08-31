with
    source as (
        select * from {{ source("hde_raw", "industry_target_filters__category_ids") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_target_filter_category_uuid,
            _dlt_parent_id::text as industry_target_filter_uuid,
            value::bigint as category_id

        from source
    )

select *
from renamed
