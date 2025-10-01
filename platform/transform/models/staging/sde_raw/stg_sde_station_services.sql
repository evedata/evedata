with
    source as (select * from {{ source("sde_raw", "station_services") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as station_service_uuid,
            id::bigint as station_service_id,

            -- -------- Text
            description_id__de::text as description_de,
            description_id__en::text as description_en,
            description_id__es::text as description_es,
            description_id__fr::text as description_fr,
            description_id__ja::text as description_ja,
            description_id__ko::text as description_ko,
            description_id__ru::text as description_ru,
            description_id__zh::text as description_zh,
            service_name_id__de::text as name_de,
            service_name_id__en::text as name_en,
            service_name_id__es::text as name_es,
            service_name_id__fr::text as name_fr,
            service_name_id__ja::text as name_ja,
            service_name_id__ko::text as name_ko,
            service_name_id__ru::text as name_ru,
            service_name_id__zh::text as name_zh,
            sde_version::text as sde_version

        from source
    )

select *
from renamed
