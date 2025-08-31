with
    type_dogma as (select * from {{ ref("stg_sde_type_dogma") }}),
    type_attributes as (select * from {{ ref("stg_sde_type_attributes") }}),

    joined as (
        select type_attributes.attribute_id, type_dogma.type_id, type_attributes.value
        from type_attributes
        inner join type_dogma on type_attributes.type_uuid = type_dogma.type_uuid
    )

select *
from joined
