with
    factions as (
        select
            faction_id,
            npc_corporation_id,
            icon_id,
            militia_npc_corporation_id,
            system_id,
            description_en as description,
            flat_logo,
            flat_logo_with_name,
            name_en as name,
            short_description_en as short_description,
            size_factor,
            has_unique_name
        from {{ ref("stg_sde_factions") }}
    )

select *
from factions
