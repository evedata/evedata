with
    source as (select * from {{ source("sde_raw", "station_operations__services") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as station_operation_service_uuid,
            _dlt_parent_id::text as station_operation_uuid,
            value::bigint as station_service_id

        from source
    )

select *
from renamed
