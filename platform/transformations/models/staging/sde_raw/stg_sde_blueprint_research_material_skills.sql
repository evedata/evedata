with
    source as (
        select *
        from
            {{ source("sde_raw", "blueprints__activities__research_material__skills") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as blueprint_research_material_skill_uuid,
            _dlt_parent_id::text as blueprint_uuid,
            type_id::bigint as type_id,

            -- -------- Numerics
            level::bigint as level

        from source
    )

select *
from renamed
