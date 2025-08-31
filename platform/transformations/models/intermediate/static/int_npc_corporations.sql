with
    npc_corporations as (
        select
            npc_corporation_id,
            ceo_id,
            enemy_corporation_id,
            faction_id,
            friend_corporation_id,
            icon_id,
            primary_activity_type_id,
            race_id,
            secondary_activity_type_id,
            station_id,
            system_id,
            description_en as description,
            extent,
            name_en as name,
            size,
            ticker,
            url,
            member_limit,
            minimum_join_standing,
            minimum_security_status,
            size_factor,
            tax_rate,
            has_player_personnel_manager,
            is_deleted,
            sends_char_termination_message
        from {{ ref("stg_sde_npc_corporations") }}
    )

select *
from npc_corporations
