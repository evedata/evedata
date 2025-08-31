with
    source as (
        select * from {{ source("hde_raw", "dbuffs__location_group_modifiers") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as buff_location_group_modifier_uuid,
            _dlt_parent_id::text as dbuff_uuid,
            attribute_id::bigint as attribute_id,
            group_id::bigint as group_id

        from source
    )

select *
from renamed
