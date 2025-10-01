with
    source as (
        select * from {{ source("sde_raw", "station_operations__station_types") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as station_operation_station_type_uuid,
            _dlt_parent_id::text as station_operation_uuid,
            id::bigint as race_id,
            value::bigint as type_id

        from source
    )

select *
from renamed
