with
    source as (select * from {{ source("sde_raw", "types__masteries") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_mastery_level_uuid,
            _dlt_parent_id::text as type_mastery_uuid,

            -- -------- Numerics
            id::bigint as level

        from source
    )

select *
from renamed
