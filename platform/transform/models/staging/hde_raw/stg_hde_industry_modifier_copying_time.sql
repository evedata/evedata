with
    source as (
        select *
        from {{ source("hde_raw", "industry_modifier_sources__copying__time") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_modifier_copying_time_uuid,
            _dlt_parent_id::text as industry_modifier_source_uuid,
            dogma_attribute_id::bigint as attribute_id

        from source
    )

select *
from renamed
