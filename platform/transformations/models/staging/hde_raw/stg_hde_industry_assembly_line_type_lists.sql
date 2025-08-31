with
    source as (
        select *
        from {{ source("hde_raw", "industry_assembly_lines__details_per_type_list") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_assembly_line_type_list_uuid,
            _dlt_parent_id::text as industry_assembly_line_uuid,
            type_list_id::bigint as type_list_id,

            -- -------- Numerics
            material_multiplier::decimal as material_multiplier,
            time_multiplier::decimal as time_multiplier

        from source
    )

select *
from renamed
