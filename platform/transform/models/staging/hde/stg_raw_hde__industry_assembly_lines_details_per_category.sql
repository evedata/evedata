with
    source as (

        select *
        from {{ source("raw_hde", "industryassemblylines__details_per_category") }}

    ),

    renamed as (

        select
            time_multiplier,
            material_multiplier,
            category_id,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id,
            cost_multiplier

        from source

    )

select *
from renamed
