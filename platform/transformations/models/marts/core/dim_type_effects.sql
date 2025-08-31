with
    effects as (select * from {{ ref("int_effects") }}),
    effect_categories as (select * from {{ ref("stg_hde_effect_categories") }}),
    type_effects as (select * from {{ ref("int_type_effects") }}),
    types as (select type_id from {{ ref("dim_types") }}),

    joined as (
        select
            effects.*,
            {{
                dbt_utils.generate_surrogate_key(
                    ["effects.effect_id", "types.type_id"]
                )
            }} as type_effect_key,
            types.type_key,
            effect_categories.effect_category_id,
            effect_categories.name as effect_category_name,
            type_effects.is_default
        from type_effects
        inner join types on type_effects.type_id = types.type_id
        inner join effects on type_effects.effect_id = effects.effect_id
        inner join
            effect_categories
            on effects.effect_category_id = effect_categories.effect_category_id
    )

select *
from joined
