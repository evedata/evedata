with
    source as (select * from {{ source("sde_raw", "races__skills") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as race_skill_uuid,
            _dlt_parent_id::text as race_uuid,
            id::bigint as type_id,

            -- -------- Numerics
            value::bigint as level

        from source
    )

select *
from renamed
