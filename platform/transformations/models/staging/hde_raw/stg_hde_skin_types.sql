with
    source as (select * from {{ source("hde_raw", "skins__types") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as skin_type_uuid,
            _dlt_parent_id::text as skin_uuid,
            value::bigint as type_id

        from source
    )

select *
from renamed
