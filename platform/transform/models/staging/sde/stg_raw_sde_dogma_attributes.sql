with
    source as (select * from {{ source("raw_sde", "dogma_attributes") }}),

    renamed as (

        select
            _key as dogma_attribute_id,
            attribute_category_id,
            data_type,
            default_value,
            description,
            display_when_zero,
            high_is_good,
            name,
            published,
            stackable,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            display_name__de,
            display_name__en,
            display_name__es,
            display_name__fr,
            display_name__ja,
            display_name__ko,
            display_name__ru,
            display_name__zh,
            icon_id,
            tooltip_description__de,
            tooltip_description__en,
            tooltip_description__es,
            tooltip_description__fr,
            tooltip_description__ja,
            tooltip_description__ko,
            tooltip_description__ru,
            tooltip_description__zh,
            tooltip_title__de,
            tooltip_title__en,
            tooltip_title__es,
            tooltip_title__fr,
            tooltip_title__ja,
            tooltip_title__ko,
            tooltip_title__ru,
            tooltip_title__zh,
            unit_id,
            charge_recharge_time_id,
            max_attribute_id,
            min_attribute_id

        from source

    )

select *
from renamed
