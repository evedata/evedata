with
    source as (select * from {{ source("sde_raw", "inv_unique_names") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as item_name_uuid,
            item_id::bigint as item_id,
            group_id::bigint as group_id,

            -- -------- Text
            item_name::text as name,
            sde_version::text as sde_version

        from source
    )

select *
from renamed
