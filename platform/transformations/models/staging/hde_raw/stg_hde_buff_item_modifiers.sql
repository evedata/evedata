with
    source as (select * from {{ source("hde_raw", "dbuffs__item_modifiers") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as buff_item_modifier_uuid,
            _dlt_parent_id::text as dbuff_uuid,
            attribute_id::bigint as attribute_id

        from source
    )

select *
from renamed
