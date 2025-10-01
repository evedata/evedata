with
    source as (select * from {{ source("hde_raw", "schools__starting_stations") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as school_starting_station_uuid,
            _dlt_parent_id::text as school_uuid,
            value::bigint as station_id

        from source
    )

select *
from renamed
