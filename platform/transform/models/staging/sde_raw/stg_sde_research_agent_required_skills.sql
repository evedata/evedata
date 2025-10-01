with
    source as (select * from {{ source("sde_raw", "research_agents__skills") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as research_agent_required_skill_uuid,
            _dlt_parent_id::text as research_agent_uuid,
            type_id::bigint as type_id

        from source
    )

select *
from renamed
