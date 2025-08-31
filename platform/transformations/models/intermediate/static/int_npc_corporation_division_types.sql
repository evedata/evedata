with
    npc_corporation_division_types as (
        select
            npc_corporation_division_type_id,
            description_en as description,
            internal_name,
            leader_type_name_en,
            name_en as name,
            short_description
        from {{ ref("stg_sde_npc_corporation_division_types") }}
    )

select *
from npc_corporation_division_types
