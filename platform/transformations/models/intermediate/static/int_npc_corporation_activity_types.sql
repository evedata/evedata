with
    npc_corporation_activity_types as (
        select npc_corporation_activity_type_id, name_en as name
        from {{ ref("stg_sde_npc_corporation_activity_types") }}
    )

select *
from npc_corporation_activity_types
