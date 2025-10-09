with
    source as (select * from {{ source("raw_sde", "npc_corporations") }}),

    renamed as (

        select
            _key as npc_corporation_id,
            ceo_id,
            deleted,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            extent,
            has_player_personnel_manager,
            initial_price,
            member_limit,
            min_security,
            minimum_join_standing,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            send_char_termination_message,
            shares,
            size,
            station_id,
            tax_rate,
            ticker_name,
            unique_name,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            enemy_id,
            faction_id,
            friend_id,
            icon_id,
            main_activity_id,
            race_id,
            size_factor,
            solar_system_id,
            secondary_activity_id

        from source

    )

select *
from renamed
