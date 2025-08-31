with
    type_bonuses as (select * from {{ ref("int_type_bonuses") }}),
    types as (select type_id from {{ ref("dim_types") }}),

    joined as (
        select type_bonuses.*, types.type_key, bonus_types.type_key as bonus_type_key
        from type_bonuses
        inner join types on type_bonuses.type_id = types.type_id
        inner join
            types as bonus_types on type_bonuses.bonus_type_id = bonus_types.type_id
    )

select *
from joined
