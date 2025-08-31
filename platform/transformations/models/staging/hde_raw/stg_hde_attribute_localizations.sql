with
    source as (select * from {{ source("hde_raw", "localization_dogma_attributes") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as attribute_localization_uuid,
            id::bigint as attribute_id,

            -- -------- Text
            de__display_name::text as display_name_de,
            en_us__display_name::text as display_name_en,
            es__display_name::text as display_name_es,
            fr__display_name::text as display_name_fr,
            it__display_name::text as display_name_it,
            ja__display_name::text as display_name_ja,
            ko__display_name::text as display_name_ko,
            ru__display_name::text as display_name_ru,
            zh__display_name::text as display_name_zh,
            de__description::text as description_de,
            en_us__description::text as description_en,
            es__description::text as description_es,
            fr__description::text as description_fr,
            it__description::text as description_it,
            ja__description::text as description_ja,
            ko__description::text as description_ko,
            ru__description::text as description_ru,
            zh__description::text as description_zh

        from source
    )

select *
from renamed
