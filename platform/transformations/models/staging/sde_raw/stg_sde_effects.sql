with
    source as (select * from {{ source("sde_raw", "dogma_effects") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as effect_uuid,
            id::bigint as effect_id,
            discharge_attribute_id::bigint as discharge_attribute_id,
            duration_attribute_id::bigint as duration_attribute_id,
            effect_category::bigint as effect_category_id,
            falloff_attribute_id::bigint as falloff_attribute_id,
            fitting_usage_chance_attribute_id::bigint
            as fitting_usage_chance_attribute_id,
            icon_id::bigint as icon_id,
            npc_activation_chance_attribute_id::bigint
            as npc_activation_chance_attribute_id,
            npc_usage_chance_attribute_id::bigint as npc_usage_chance_attribute_id,
            range_attribute_id::bigint as range_attribute_id,
            resistance_attribute_id::bigint as resistance_attribute_id,
            tracking_speed_attribute_id::bigint as tracking_speed_attribute_id,

            -- -------- Text
            description_id__de::text as description_de,
            description_id__en::text as description_en,
            description_id__es::text as description_es,
            description_id__fr::text as description_fr,
            description_id__ja::text as description_ja,
            description_id__ko::text as description_ko,
            description_id__ru::text as description_ru,
            description_id__zh::text as description_zh,
            display_name_id__de::text as display_name_de,
            display_name_id__en::text as display_name_en,
            display_name_id__es::text as display_name_es,
            display_name_id__fr::text as display_name_fr,
            display_name_id__ja::text as display_name_ja,
            display_name_id__ko::text as display_name_ko,
            display_name_id__ru::text as display_name_ru,
            display_name_id__zh::text as display_name_zh,
            effect_name::text as internal_name,
            guid::text as guid,
            sde_version::text as sde_version,
            sfx_name::text as sfx_name,

            -- -------- Numerics
            distribution::bigint as distribution,

            -- -------- Booleans
            disallow_auto_repeat::boolean as disallows_auto_repeat,
            electronic_chance::boolean as has_electronic_chance,
            propulsion_chance::boolean as has_propulsion_chance,
            range_chance::boolean as has_range_chance,
            is_assistance::boolean as is_assistance,
            is_offensive::boolean as is_offensive,
            is_warp_safe::boolean as is_warp_safe,
            published::boolean as is_published

        from source
    )

select *
from renamed
