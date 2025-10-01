with
    source as (
        select * from {{ source("hde_raw", "skill_plans__skill_requirements") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as skill_plan_requirement_uuid,
            _dlt_parent_id::text as skill_plan_uuid,
            type_id::bigint as type_id,

            -- -------- Numerics
            level::bigint as level

        from source
    )

select *
from renamed
