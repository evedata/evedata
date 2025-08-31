with
    attributes as (
        select
            attribute_id,
            charge_time_attribute_id,
            dogma_attribute_category_id,
            unit_id,
            icon_id,
            max_attribute_id,
            min_attribute_id,
            data_type_id,
            description,
            display_name_en as display_name,
            internal_name,
            tooltip_description_en as tooltip_description,
            tooltip_title_en as tooltip_title,
            default_value,
            display_when_zero,
            high_is_good,
            is_published,
            is_stackable
        from {{ ref("stg_sde_attributes") }}
    )

select *
from attributes
