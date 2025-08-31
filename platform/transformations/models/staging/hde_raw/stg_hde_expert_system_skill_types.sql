with
    source as (select * from {{ source("hde_raw", "expert_systems__skills_granted") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as expert_system_skill_uuid,
            _dlt_parent_id::text as expert_system_uuid,
            id::bigint as type_id,

            -- -------- Numerics
            value::bigint as level

        from source
    )

select *
from renamed
