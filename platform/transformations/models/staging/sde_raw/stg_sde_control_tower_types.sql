with
    source as (select * from {{ source("sde_raw", "control_tower_resources") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as control_tower_type_uuid, id::bigint as type_id

        from source
    )

select *
from renamed
