with
    effects as (
        select
            effect_id,
            discharge_attribute_id,
            effect_category_id,
            duration_attribute_id,
            falloff_attribute_id,
            fitting_usage_chance_attribute_id,
            icon_id,
            npc_activation_chance_attribute_id,
            npc_usage_chance_attribute_id,
            range_attribute_id,
            resistance_attribute_id,
            tracking_speed_attribute_id,

            -- -------- Text
            description_en as description,
            display_name_en as display_name,
            internal_name,
            guid,
            sfx_name,

            -- -------- Numerics
            distribution,

            -- -------- Booleans
            disallows_auto_repeat,
            has_electronic_chance,
            has_propulsion_chance,
            has_range_chance,
            is_assistance,
            is_offensive,
            is_warp_safe,
            is_published

        from {{ ref("stg_sde_effects") }}
        where valid_to is null
    )

select *
from effects
