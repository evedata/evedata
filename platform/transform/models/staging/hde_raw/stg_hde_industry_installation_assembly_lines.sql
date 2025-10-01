with
    source as (
        select *
        from {{ source("hde_raw", "industry_installation_types__assembly_lines") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_installation_assembly_line_uuid,
            _dlt_parent_id::text as industry_installation_uuid,
            assembly_line::bigint as industry_assembly_line_id

        from source
    )

select *
from renamed
