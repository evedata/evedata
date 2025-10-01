with
    source as (
        select *
        from {{ source("hde_raw", "industry_modifier_sources__reaction__material") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_modifier_reaction_material_uuid,
            _dlt_parent_id::text as industry_modifier_source_uuid,
            dogma_attribute_id::bigint as attribute_id,
            filter_id::bigint as filter_id

        from source
    )

select *
from renamed
