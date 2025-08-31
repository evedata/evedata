with
    source as (select * from {{ source("hde_raw", "school_map") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as school_map_uuid,
            id::bigint as school_map_id,
            solar_system_id::bigint as system_id,
            school_id::bigint as school_id

        from source
    )

select *
from renamed
