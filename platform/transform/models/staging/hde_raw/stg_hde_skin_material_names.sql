with
    source as (select * from {{ source("hde_raw", "skin_material_names") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as skin_material_uuid,
            key::bigint as skin_material_id,

            -- -------- Text
            hde_version::text as hde_version,
            value::text as name

        from source
    )

select *
from renamed
