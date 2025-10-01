with
    source as (select * from {{ source("sde_raw", "types__traits__role_bonuses") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_role_bonus_uuid,
            _dlt_parent_id::text as type_uuid,
            _dlt_list_idx::smallint as bonus_index,
            unit_id::bigint as unit_id,

            -- -------- Text
            bonus_text__de::text as description_de,
            bonus_text__en::text as description_en,
            bonus_text__es::text as description_es,
            bonus_text__fr::text as description_fr,
            bonus_text__ja::text as description_ja,
            bonus_text__ko::text as description_ko,
            bonus_text__ru::text as description_ru,
            bonus_text__zh::text as description_zh,

            -- -------- Numerics
            bonus::decimal as bonus,
            importance::bigint as importance

        from source
    )

select *
from renamed
