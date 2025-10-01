{{ config(materialized="table") }}

with
    attributes as (
        select
            attribute_id,
            charge_time_attribute_id,
            attribute_category_id,
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
            is_stackable,
            sde_version
        from {{ ref("stg_sde_attributes") }}
    ),

    attributes_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from attributes
        window w as (partition by attribute_id order by sde_version)
    ),

    final as (
        select
            *,

            {{ dbt_utils.generate_surrogate_key(["attribute_id", "from_sde_version"]) }}
            as attribute_sk,
            coalesce(to_sde_version is null, false) as is_current
        from attributes_scd2
    )

select *
from final
