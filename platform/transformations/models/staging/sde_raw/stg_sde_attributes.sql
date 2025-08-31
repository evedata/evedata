with
    source as (select * from {{ source("sde_raw", "dogma_attributes") }}),

    renamed as (
        select
            _dlt_id::text as attribute_uuid,
            id::bigint as attribute_id,
            category_id::bigint as attribute_category_id,
            charge_recharge_time_id::bigint as charge_time_attribute_id,
            unit_id::bigint as unit_id,
            icon_id::bigint as icon_id,
            max_attribute_id::bigint as max_attribute_id,
            min_attribute_id::bigint as min_attribute_id,
            data_type::bigint as data_type_id,
            description::text as description,
            display_name_id__de::text as display_name_de,
            display_name_id__en::text as display_name_en,
            display_name_id__es::text as display_name_es,
            display_name_id__fr::text as display_name_fr,
            display_name_id__ja::text as display_name_ja,
            display_name_id__ko::text as display_name_ko,
            display_name_id__ru::text as display_name_ru,
            display_name_id__zh::text as display_name_zh,
            name::text as internal_name,
            tooltip_description_id__de::text as tooltip_description_de,
            tooltip_description_id__en::text as tooltip_description_en,
            tooltip_description_id__es::text as tooltip_description_es,
            tooltip_description_id__fr::text as tooltip_description_fr,
            tooltip_description_id__ja::text as tooltip_description_ja,
            tooltip_description_id__ko::text as tooltip_description_ko,
            tooltip_description_id__ru::text as tooltip_description_ru,
            tooltip_description_id__zh::text as tooltip_description_zh,
            tooltip_title_id__de::text as tooltip_title_de,
            tooltip_title_id__en::text as tooltip_title_en,
            tooltip_title_id__es::text as tooltip_title_es,
            tooltip_title_id__fr::text as tooltip_title_fr,
            tooltip_title_id__ja::text as tooltip_title_ja,
            tooltip_title_id__ko::text as tooltip_title_ko,
            tooltip_title_id__ru::text as tooltip_title_ru,
            tooltip_title_id__zh::text as tooltip_title_zh,
            default_value::decimal as default_value,
            display_when_zero::boolean as display_when_zero,
            high_is_good::boolean as high_is_good,
            published::boolean as is_published,
            stackable::boolean as is_stackable
        from source
    )

select *
from renamed
