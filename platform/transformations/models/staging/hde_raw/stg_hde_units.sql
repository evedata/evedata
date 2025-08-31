with
    source as (select * from {{ source("hde_raw", "dogma_units") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as unit_uuid,
            id::bigint as unit_id,

            -- -------- Text
            description::text as description,
            display_name::text as display_name,
            name::text as name

        from source
    )

select *
from renamed
