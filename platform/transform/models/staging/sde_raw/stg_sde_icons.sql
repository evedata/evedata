with
    source as (select * from {{ source("sde_raw", "icons") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as icon_uuid,
            id::bigint as icon_id,

            -- -------- Text
            description::text as description,
            icon_file::text as icon_file,
            sde_version::text as sde_version,

            -- -------- Booleans
            obsolete::boolean as is_obsolete

        from source
    )

select *
from renamed
