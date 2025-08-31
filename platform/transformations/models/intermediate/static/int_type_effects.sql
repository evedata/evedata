with
    type_dogma as (select * from {{ ref("stg_sde_type_dogma") }}),
    type_effects as (select * from {{ ref("stg_sde_type_effects") }}),

    joined as (
        select type_effects.effect_id, type_dogma.type_id, type_effects.is_default
        from type_effects
        inner join type_dogma on type_effects.type_uuid = type_dogma.type_uuid
    )

select *
from joined
