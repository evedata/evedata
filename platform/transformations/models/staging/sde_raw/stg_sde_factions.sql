with
    source as (select * from {{ source("sde_raw", "factions") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as faction_uuid,
            id::bigint as faction_id,
            corporation_id::bigint as npc_corporation_id,
            icon_id::bigint as icon_id,
            militia_corporation_id::bigint as militia_npc_corporation_id,
            solar_system_id::bigint as system_id,

            -- -------- Text
            description_id__de::text as description_de,
            description_id__en::text as description_en,
            description_id__es::text as description_es,
            description_id__fr::text as description_fr,
            description_id__ja::text as description_ja,
            description_id__ko::text as description_ko,
            description_id__ru::text as description_ru,
            description_id__zh::text as description_zh,
            flat_logo::text as flat_logo,
            flat_logo_with_name::text as flat_logo_with_name,
            name_id__de::text as name_de,
            name_id__en::text as name_en,
            name_id__es::text as name_es,
            name_id__fr::text as name_fr,
            name_id__it::text as name_it,
            name_id__ja::text as name_ja,
            name_id__ko::text as name_ko,
            name_id__ru::text as name_ru,
            name_id__zh::text as name_zh,
            short_description_id__de::text as short_description_de,
            short_description_id__en::text as short_description_en,
            short_description_id__es::text as short_description_es,
            short_description_id__fr::text as short_description_fr,
            short_description_id__ja::text as short_description_ja,
            short_description_id__ko::text as short_description_ko,
            short_description_id__ru::text as short_description_ru,
            short_description_id__zh::text as short_description_zh,

            -- -------- Numerics
            size_factor::decimal as size_factor,

            -- -------- Booleans
            unique_name::boolean as has_unique_name

        from source
    )

select *
from renamed
