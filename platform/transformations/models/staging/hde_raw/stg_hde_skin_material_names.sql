with
    source as (select * from {{ source("hde_raw", "skin_material_names") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as skin_material_uuid,
            key::bigint as skin_material_id,

            -- -------- Text
            value::text as name

        from source
    )

select *
from renamed
