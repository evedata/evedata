with
    names as (select * from {{ ref("stg_sde_item_names") }}),
    research_agents as (select * from {{ ref("stg_sde_research_agents") }}),

    agents as (
        select
            agent_id,
            agent_type_id,
            npc_corporation_id,
            npc_corporation_division_id,
            station_id,
            level,
            is_locator
        from {{ ref("stg_sde_agents") }}
    ),

    joined as (
        select
            agents.*,
            names.name,
            research_agents.research_agent_id is not null as is_research
        from agents
        left join names on agents.agent_id = names.item_id
        left join research_agents on agents.agent_id = research_agents.research_agent_id
    )

select *
from joined
