with
    source as (select * from {{ source("sde_raw", "contraband_types") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as contraband_type_uuid,
            id::bigint as type_id,

            -- -------- Text
            sde_version::text as sde_version

        from source
    )

select *
from renamed
