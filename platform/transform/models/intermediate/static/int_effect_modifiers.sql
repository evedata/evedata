with
    effect_modifiers as (
        select

            -- -------- IDs
            de.effect_id,
            dem.effect_modifier_index,
            dem.group_id,
            dem.modified_attribute_id,
            dem.modifying_attribute_id,
            dem.skill_type_id,

            -- -------- Text
            dem.domain,
            dem.func,
            dem.operator

        from {{ ref("stg_sde_effect_modifiers") }} as dem
        inner join
            {{ ref("stg_sde_effects") }} as de on dem.effect_uuid = de.effect_uuid
    )

select *
from effect_modifiers
