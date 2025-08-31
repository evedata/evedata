with
    source as (select * from {{ source("sde_raw", "landmarks") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as landmark_uuid,
            id::bigint as landmark_id,
            icon_id::bigint as icon_id,
            description_id::bigint as description_id,
            landmark_name_id::bigint as landmark_name_id,
            location_id::bigint as system_id

        from source
    )

select *
from renamed
