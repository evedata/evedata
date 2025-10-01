with
    source as (select * from {{ source("sde_raw", "categories") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as category_uuid,
            id::bigint as category_id,
            icon_id::bigint as icon_id,

            -- -------- Text
            name__de::text as name_de,
            name__en::text as name_en,
            name__es::text as name_es,
            name__fr::text as name_fr,
            name__ja::text as name_ja,
            name__ko::text as name_ko,
            name__ru::text as name_ru,
            name__zh::text as name_zh,
            sde_version::text as sde_version,

            -- -------- Booleans
            published::boolean as is_published

        from source
    )

select *
from renamed
