with
    source as (select * from {{ source("sde_raw", "groups") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as group_uuid,
            id::bigint as group_id,
            category_id::bigint as category_id,
            icon_id::bigint as icon_id,

            -- -------- Text
            name__de::text as name_de,
            name__en::text as name_en,
            name__es::text as name_es,
            name__fr::text as name_fr,
            name__it::text as name_it,
            name__ja::text as name_ja,
            name__ko::text as name_ko,
            name__ru::text as name_ru,
            name__zh::text as name_zh,

            -- -------- Booleans
            anchorable::boolean as is_anchorable,
            anchored::boolean as is_anchored,
            fittable_non_singleton::boolean as is_fittable_non_singleton,
            published::boolean as is_published,
            use_base_price::boolean as uses_base_price

        from source
    )

select *
from renamed
