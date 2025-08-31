with
    source as (
        select *
        from {{ source("hde_raw", "dbuffs__location_required_skill_modifiers") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as buff_location_required_skill_modifier_uuid,
            _dlt_parent_id::text as buff_uuid,
            attribute_id::bigint as attribute_id,
            skill_id::bigint as type_id

        from source
    )

select *
from renamed
