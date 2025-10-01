with
    source as (select * from {{ source("hde_raw", "industry_assembly_lines") }}),

    renamed as (
        select

            -- -------- IDs
            id::bigint as industry_assembly_line_id,
            activity::bigint as industry_activity_id,

            -- -------- Text
            description::text as description,
            hde_version::text as hde_version,
            name::text as name,

            -- -------- Numerics
            base_cost_multiplier::decimal as base_cost_multiplier,
            base_material_multiplier::decimal as base_material_multiplier,
            base_time_multiplier::decimal as base_time_multiplier

        from source
    )

select *
from renamed
