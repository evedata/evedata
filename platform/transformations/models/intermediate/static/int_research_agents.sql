with
    agents as (select * from {{ ref("stg_sde_agents") }}),
    items as (select * from {{ ref("stg_sde_items") }}),
    names as (select * from {{ ref("stg_sde_item_names") }}),
    research_agents as (select * from {{ ref("stg_sde_research_agents") }}),
    stations as (select * from {{ ref("stg_sde_stations") }}),

    joined as (
        select
            research_agents.research_agent_id,
            agents.agent_type_id,
            names.name,
            agents.level,
            agents.is_locator,
            true as is_research,

            coalesce(agents.station_id, stations.station_id) as station_id,
            coalesce(
                agents.npc_corporation_id, stations.npc_corporation_id
            ) as npc_corporation_id,
            coalesce(
                agents.npc_corporation_division_id, 18
            ) as npc_corporation_division_id
        from research_agents
        left join agents on research_agents.research_agent_id = agents.agent_id
        left join names on research_agents.research_agent_id = names.item_id
        left join items on research_agents.research_agent_id = items.item_id
        left join stations on items.location_id = stations.station_id
    )

select *
from joined
