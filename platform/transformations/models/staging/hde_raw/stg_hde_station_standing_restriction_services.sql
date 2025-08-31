with
    source as (
        select *
        from {{ source("hde_raw", "station_standings_restrictions__services") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as station_standing_restriction_uuid,
            _dlt_parent_id::text as station_standing_uuid,
            id::bigint as station_service_id,

            -- -------- Numerics
            value::decimal as standing

        from source
    )

select *
from renamed
