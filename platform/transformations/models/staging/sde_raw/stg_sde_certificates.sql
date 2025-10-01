with
    source as (select * from {{ source("sde_raw", "certificates") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as certificate_uuid,
            id::bigint as certificate_id,
            group_id::bigint as group_id,

            -- -------- Text
            description::text as description,
            name::text as name,
            sde_version::text as sde_version

        from source
    )

select *
from renamed
