with
    source as (select * from {{ source("hde_raw", "station_standings_restrictions") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as station_standing_uuid, id::bigint as station_id

        from source
    )

select *
from renamed
