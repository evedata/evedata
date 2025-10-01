{{ config(materialized="table") }}

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
            sde_version,
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
    ),

    effects_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from effects
        window w as (partition by effect_id order by sde_version)
    ),

    final as (
        select
            *,
            {{ dbt_utils.generate_surrogate_key(["effect_id", "from_sde_version"]) }}
            as effect_sk,
            coalesce(to_sde_version is null, false) as is_current
        from effects_scd2
    )

select *
from final
