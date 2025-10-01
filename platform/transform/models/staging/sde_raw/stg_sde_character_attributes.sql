with
    source as (select * from {{ source("sde_raw", "character_attributes") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as character_attribute_uuid,
            id::bigint as character_attribute_id,
            icon_id::bigint as icon_id,

            -- -------- Text
            description::text as description,
            name_id__de::text as name_de,
            name_id__en::text as name_en,
            name_id__es::text as name_es,
            name_id__fr::text as name_fr,
            name_id__ja::text as name_ja,
            name_id__ko::text as name_ko,
            name_id__ru::text as name_ru,
            name_id__zh::text as name_zh,
            notes::text as notes,
            sde_version::text as sde_version,
            short_description::text as short_description

        from source
    )

select *
from renamed
