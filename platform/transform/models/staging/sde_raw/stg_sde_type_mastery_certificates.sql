with
    source as (select * from {{ source("sde_raw", "types__masteries__value") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_mastery_certificate_uuid,
            _dlt_parent_id::text as type_mastery_uuid,
            value::bigint as certificate_id

        from source
    )

select *
from renamed
