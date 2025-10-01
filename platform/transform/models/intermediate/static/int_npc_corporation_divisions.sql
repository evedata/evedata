with
    npc_corporation_divisions as (
        select * from {{ ref("stg_sde_npc_corporation_divisions") }}
    ),
    npc_corporations as (select * from {{ ref("stg_sde_npc_corporations") }}),

    joined as (
        select
            npc_corporations.npc_corporation_id,
            npc_corporation_divisions.npc_corporation_division_type_id,
            npc_corporation_divisions.leader_id,
            npc_corporation_divisions.division_number,
            npc_corporation_divisions.size
        from npc_corporation_divisions
        inner join
            npc_corporations
            on npc_corporation_divisions.npc_corporation_uuid
            = npc_corporations.npc_corporation_uuid
    )

select *
from joined
