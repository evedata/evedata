with
    source as (select * from {{ source("sde_raw", "types") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_uuid,
            id::bigint as type_id,
            faction_id::bigint as faction_id,
            graphic_id::bigint as graphic_id,
            group_id::bigint as group_id,
            icon_id::bigint as icon_id,
            market_group_id::bigint as market_group_id,
            meta_group_id::bigint as meta_group_id,
            race_id::bigint as race_id,
            sof_material_set_id::bigint as sof_material_set_id,
            sound_id::bigint as sound_id,
            traits__icon_id::bigint as bonus_icon_id,
            variation_parent_type_id::bigint as parent_type_id,

            -- -------- Text
            description__de::text as description_de,
            description__en::text as description_en,
            description__es::text as description_es,
            description__fr::text as description_fr,
            description__it::text as description_it,
            description__ja::text as description_ja,
            description__ko::text as description_ko,
            description__ru::text as description_ru,
            description__zh::text as description_zh,
            name__de::text as name_de,
            name__en::text as name_en,
            name__es::text as name_es,
            name__fr::text as name_fr,
            name__it::text as name_it,
            name__ja::text as name_ja,
            name__ko::text as name_ko,
            name__ru::text as name_ru,
            name__zh::text as name_zh,
            sof_faction_name::text as sof_faction_name,

            -- -------- Numerics
            base_price::decimal as base_price,
            capacity::decimal as capacity,
            mass::decimal as mass,
            portion_size::bigint as portion_size,
            radius::decimal as radius,
            volume::decimal as volume,

            -- -------- Booleans
            published::boolean as is_published

        from source
    )

select *
from renamed
