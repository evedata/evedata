with
    source as (select * from {{ source("sde_raw", "type_dogma") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_dogma_uuid,
            id::bigint as type_id,

            -- -------- Text
            sde_version::text as sde_version

        from source
    )

select *
from renamed
