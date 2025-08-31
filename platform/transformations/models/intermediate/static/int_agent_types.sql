with agent_types as (select agent_type_id, name from {{ ref("stg_hde_agent_types") }})

select *
from agent_types
