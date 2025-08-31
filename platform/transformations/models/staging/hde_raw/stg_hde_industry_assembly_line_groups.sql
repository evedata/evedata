with
    source as (
        select *
        from {{ source("hde_raw", "industry_assembly_lines__details_per_group") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_assembly_line_group_uuid,
            _dlt_parent_id::text as industry_assembly_line_uuid,
            group_id::bigint as group_id,

            -- -------- Numerics
            cost_multiplier::decimal as cost_multiplier,
            material_multiplier::decimal as material_multiplier,
            time_multiplier::decimal as time_multiplier

        from source
    )

select *
from renamed
