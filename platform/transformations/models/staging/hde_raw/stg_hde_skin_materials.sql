with
    source as (select * from {{ source("hde_raw", "skin_materials") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as skin_material_uuid,
            skin_material_id::bigint as skin_material_id,
            material_set_id::bigint as material_set_id,
            display_name_id::bigint as display_name_id,

            -- -------- Text
            hde_version::text as hde_version

        from source
    )

select *
from renamed
