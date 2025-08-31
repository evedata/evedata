with
    source as (
        select *
        from {{ source("sde_raw", "solar_systems__disallowed_anchor_categories") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as system_banned_anchor_category_uuid,
            _dlt_parent_id::text as system_uuid,
            value::bigint as category_id

        from source
    )

select *
from renamed
