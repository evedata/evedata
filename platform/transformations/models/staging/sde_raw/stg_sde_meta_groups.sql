with
    source as (select * from {{ source("sde_raw", "meta_groups") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as meta_group_uuid,
            id::bigint as meta_group_id,
            icon_id::bigint as icon_id,

            -- -------- Text
            description_id__de::text as description_de,
            description_id__en::text as description_en,
            description_id__es::text as description_es,
            description_id__fr::text as description_fr,
            description_id__ja::text as description_ja,
            description_id__ko::text as description_ko,
            description_id__ru::text as description_ru,
            description_id__zh::text as description_zh,
            icon_suffix::text as icon_suffix,
            name_id__de::text as name_de,
            name_id__en::text as name_en,
            name_id__es::text as name_es,
            name_id__fr::text as name_fr,
            name_id__ja::text as name_ja,
            name_id__ko::text as name_ko,
            name_id__ru::text as name_ru,
            name_id__zh::text as name_zh,
            sde_version::text as sde_version,

            -- -------- Numerics
            color__r::decimal as color_r,
            color__g::decimal as color_g,
            color__b::decimal as color_b,
            color__a::decimal as color_a

        from source
    )

select *
from renamed
