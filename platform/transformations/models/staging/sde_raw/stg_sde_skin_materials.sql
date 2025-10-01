with
    source as (select * from {{ source("sde_raw", "skin_materials") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as skin_material_uuid,
            skin_material_id::bigint as skin_material_id,
            display_name_id::bigint as display_name_id,
            material_set_id::bigint as material_set_id,

            -- -------- Text
            sde_version::text as sde_version

        from source
    )

select *
from renamed
