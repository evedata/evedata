with
    source as (select * from {{ source("hde_raw", "dbuffs__location_modifiers") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as buff_location_modifier_uuid,
            _dlt_parent_id::text as buff_uuid,
            dogma_attribute_id::bigint as attribute_id

        from source
    )

select *
from renamed
