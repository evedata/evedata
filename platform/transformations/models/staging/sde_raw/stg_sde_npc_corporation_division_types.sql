with
    source as (select * from {{ source("sde_raw", "npc_corporation_divisions") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as npc_corporation_division_type_uuid,
            id::bigint as npc_corporation_division_type_id,

            -- -------- Text
            description_id__de::text as description_de,
            description_id__en::text as description_en,
            description_id__es::text as description_es,
            description_id__fr::text as description_fr,
            description_id__ja::text as description_ja,
            description_id__ko::text as description_ko,
            description_id__ru::text as description_ru,
            description_id__zh::text as description_zh,
            internal_name::text as internal_name,
            leader_type_name_id__de::text as leader_type_name_de,
            leader_type_name_id__en::text as leader_type_name_en,
            leader_type_name_id__es::text as leader_type_name_es,
            leader_type_name_id__fr::text as leader_type_name_fr,
            leader_type_name_id__ja::text as leader_type_name_ja,
            leader_type_name_id__ko::text as leader_type_name_ko,
            leader_type_name_id__ru::text as leader_type_name_ru,
            leader_type_name_id__zh::text as leader_type_name_zh,
            name_id__de::text as name_de,
            name_id__en::text as name_en,
            name_id__es::text as name_es,
            name_id__fr::text as name_fr,
            name_id__ja::text as name_ja,
            name_id__ko::text as name_ko,
            name_id__ru::text as name_ru,
            name_id__zh::text as name_zh,
            description::text as short_description

        from source
    )

select *
from renamed
