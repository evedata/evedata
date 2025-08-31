with
    source as (select * from {{ source("hde_raw", "industry_installation_types") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_installation_type_uuid, type_id::bigint as type_id

        from source
    )

select *
from renamed
