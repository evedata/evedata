with
    source as (select * from {{ source("sde_raw", "corporation_activities") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as npc_corporation_activity_uuid,
            id::bigint as npc_corporation_activity_type_id,

            -- -------- Text
            name_id__de::text as name_de,
            name_id__en::text as name_en,
            name_id__es::text as name_es,
            name_id__fr::text as name_fr,
            name_id__ja::text as name_ja,
            name_id__ko::text as name_ko,
            name_id__ru::text as name_ru,
            name_id__zh::text as name_zh,
            sde_version::text as sde_version

        from source
    )

select *
from renamed
