with
    source as (select * from {{ source("hde_raw", "type_materials__materials") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_reprocessing_output_type_uuid,
            _dlt_parent_id::text as type_reprocessing_output_uuid,
            material_type_id::bigint as type_id,

            -- -------- Numerics
            quantity::bigint as quantity

        from source
    )

select *
from renamed
