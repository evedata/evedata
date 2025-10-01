with
    source as (
        select *
        from {{ source("sde_raw", "blueprints__activities__manufacturing__materials") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as blueprint_manufacturing_material_uuid,
            _dlt_parent_id::text as blueprint_uuid,
            type_id::bigint as type_id,

            -- -------- Numerics
            quantity::bigint as quantity

        from source
    )

select *
from renamed
