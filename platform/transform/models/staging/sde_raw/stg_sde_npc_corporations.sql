with
    source as (select * from {{ source("sde_raw", "npc_corporations") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as npc_corporation_uuid,
            id::bigint as npc_corporation_id,
            ceo_id::bigint as ceo_id,
            enemy_id::bigint as enemy_corporation_id,
            faction_id::bigint as faction_id,
            friend_id::bigint as friend_corporation_id,
            icon_id::bigint as icon_id,
            main_activity_id::bigint as primary_activity_type_id,
            race_id::bigint as race_id,
            secondary_activity_id::bigint as secondary_activity_type_id,
            station_id::bigint as station_id,
            solar_system_id::bigint as system_id,

            -- -------- JSON
            corporation_trades::json as corporation_trades,
            exchange_rates::json as exchange_rates,
            lp_offer_tables::json as lp_offer_tables,
            investors::json as investors,

            -- -------- Text
            description_id__de::text as description_de,
            description_id__en::text as description_en,
            description_id__es::text as description_es,
            description_id__fr::text as description_fr,
            description_id__it::text as description_it,
            description_id__ja::text as description_ja,
            description_id__ko::text as description_ko,
            description_id__ru::text as description_ru,
            description_id__zh::text as description_zh,
            extent::text as extent,
            name_id__de::text as name_de,
            name_id__en::text as name_en,
            name_id__es::text as name_es,
            name_id__fr::text as name_fr,
            name_id__it::text as name_it,
            name_id__ja::text as name_ja,
            name_id__ko::text as name_ko,
            name_id__ru::text as name_ru,
            name_id__zh::text as name_zh,
            sde_version::text as sde_version,
            size::text as size,
            ticker_name::text as ticker,
            url::text as url,

            -- -------- Numerics
            initial_price::bigint as initial_price,
            member_limit::bigint as member_limit,
            minimum_join_standing::bigint as minimum_join_standing,
            min_security::decimal as minimum_security_status,
            public_shares::bigint as public_shares,
            shares::bigint as shares,
            size_factor::decimal as size_factor,
            tax_rate::decimal as tax_rate,

            -- -------- Booleans
            unique_name::boolean as has_unique_name,
            has_player_personnel_manager::boolean as has_player_personnel_manager,
            deleted::boolean as is_deleted,
            send_char_termination_message::boolean as sends_char_termination_message

        from source
    )

select *
from renamed
