with
    source as (select * from {{ source("sde_raw", "station_operations") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as station_operation_uuid,
            id::bigint as station_operation_id,
            activity_id::bigint as npc_corporation_activity_id,

            -- -------- Text
            description_id__de::text as description_de,
            description_id__en::text as description_en,
            description_id__es::text as description_es,
            description_id__fr::text as description_fr,
            description_id__ja::text as description_ja,
            description_id__ko::text as description_ko,
            description_id__ru::text as description_ru,
            description_id__zh::text as description_zh,
            operation_name_id__de::text as name_de,
            operation_name_id__en::text as name_en,
            operation_name_id__es::text as name_es,
            operation_name_id__fr::text as name_fr,
            operation_name_id__ja::text as name_ja,
            operation_name_id__ko::text as name_ko,
            operation_name_id__ru::text as name_ru,
            operation_name_id__zh::text as name_zh,

            -- -------- Numerics
            border::decimal as border_cost_modifier,
            corridor::decimal as corridor_cost_modifier,
            fringe::decimal as fringe_cost_modifier,
            hub::decimal as hub_cost_modifier,
            manufacturing_factor::decimal as manufacturing_factor,
            ratio::decimal as efficiency_ratio,
            research_factor::decimal as research_factor

        from source
    )

select *
from renamed
