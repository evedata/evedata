with
    source as (select * from {{ source("sde_raw", "inv_items") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as item_uuid,
            item_id::bigint as item_id,
            flag_id::bigint as flag_id,
            location_id::bigint as location_id,
            type_id::bigint as type_id,
            owner_id::bigint as parent_item_id,

            -- -------- Text
            sde_version::text as sde_version,

            -- -------- Numerics
            quantity::bigint as quantity

        from source
    )

select *
from renamed
