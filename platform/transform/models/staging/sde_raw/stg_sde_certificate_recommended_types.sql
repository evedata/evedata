with
    source as (select * from {{ source("sde_raw", "certificates__recommended_for") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as certificate_recommended_type_uuid,
            _dlt_parent_id::text as certificate_uuid,
            value::bigint as type_id

        from source
    )

select *
from renamed
