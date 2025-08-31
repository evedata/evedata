with
    source as (select * from {{ source("sde_raw", "research_agents") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as research_agent_uuid, id::bigint as research_agent_id

        from source
    )

select *
from renamed
