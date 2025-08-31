with
    source as (select * from {{ source("hde_raw", "industry_modifier_sources") }}),

    renamed as (

        select
            -- -------- IDs
            _dlt_id::text as industry_modifier_source_uuid, id::bigint as type_id

        from source
    )

select *
from renamed
