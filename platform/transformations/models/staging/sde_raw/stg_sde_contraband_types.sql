with
    source as (select * from {{ source("sde_raw", "contraband_types") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as contraband_type_uuid, id::bigint as type_id

        from source
    )

select *
from renamed
