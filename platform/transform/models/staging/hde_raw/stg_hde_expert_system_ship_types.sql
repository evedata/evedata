with
    source as (
        select * from {{ source("hde_raw", "expert_systems__associated_ship_types") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as expert_system_ship_type_uuid,
            _dlt_parent_id::text as expert_system_uuid,
            value::bigint as type_id

        from source
    )

select *
from renamed
