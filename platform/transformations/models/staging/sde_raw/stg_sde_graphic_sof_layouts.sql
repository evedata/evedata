with
    source as (select * from {{ source("sde_raw", "graphics__sof_layout") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as graphic_sof_layout_uuid,
            _dlt_parent_id::text as graphic_uuid,

            -- -------- Text
            value::text as name

        from source
    )

select *
from renamed
