with
    source as (select * from {{ source("sde_raw", "inv_names") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as item_name_uuid,
            item_id::bigint as item_id,

            -- -------- Text
            item_name::text as name

        from source
    )

select *
from renamed
