with
    source as (select * from {{ source("sde_raw", "inv_flags") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as flag_uuid,
            flag_id::bigint as flag_id,
            order_id::bigint as order_id,

            -- -------- Text
            flag_name::text as name,
            flag_text::text as description,
            sde_version::text as sde_version

        from source
    )

select *
from renamed
