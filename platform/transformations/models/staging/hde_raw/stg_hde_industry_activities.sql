with
    source as (select * from {{ source("hde_raw", "industry_activities") }}),

    renamed as (
        select

            -- -------- IDs
            activity_id::smallint as industry_activity_id,

            -- -------- Text
            activity_name::text as name,
            description::text as description,
            hde_version::text as hde_version

        from source
    )

select *
from renamed
