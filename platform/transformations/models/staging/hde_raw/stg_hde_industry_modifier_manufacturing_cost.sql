with
    source as (
        select *
        from {{ source("hde_raw", "industry_modifier_sources__manufacturing__cost") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_modifier_manufacturing_cost_uuid,
            _dlt_parent_id::text as industry_modifier_source_uuid,
            attribute_id::bigint as attribute_id

        from source
    )

select *
from renamed
