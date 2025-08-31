with
    attributes as (select * from {{ ref("int_attributes") }}),
    attribute_categories as (select * from {{ ref("stg_sde_attribute_categories") }}),
    type_attributes as (select * from {{ ref("int_type_attributes") }}),
    types as (select type_id from {{ ref("dim_types") }}),

    joined as (
        select
            attributes.*,
            {{
                dbt_utils.generate_surrogate_key(
                    ["attributes.attribute_id", "types.type_id"]
                )
            }} as type_attribute_key,
            types.type_key,
            attribute_categories.attribute_category_id,
            attribute_categories.name as attribute_category_name,
            type_attributes.value
        from type_attributes
        inner join types on type_attributes.type_id = types.type_id
        inner join attributes on type_attributes.attribute_id = attributes.attribute_id
        inner join
            attribute_categories
            on attributes.attribute_category_id
            = attribute_categories.attribute_category_id
    )

select *
from joined
