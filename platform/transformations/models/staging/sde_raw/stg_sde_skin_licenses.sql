with
    source as (select * from {{ source("sde_raw", "skin_licenses") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as skin_license_uuid,
            license_type_id::bigint as type_id,
            skin_id::bigint as skin_id,

            -- -------- Numerics
            duration::bigint as duration,

            -- -------- Booleans
            is_single_use::boolean as is_single_use

        from source
    )

select *
from renamed
