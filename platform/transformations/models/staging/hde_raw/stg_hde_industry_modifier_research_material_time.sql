with
    source as (
        select *
        from
            {{
                source(
                    "hde_raw", "industry_modifier_sources__research_material__time"
                )
            }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_modifier_research_material_time_uuid,
            _dlt_parent_id::text as industry_modifier_source_uuid,
            attribute_id::bigint as attribute_id

        from source
    )

select *
from renamed
