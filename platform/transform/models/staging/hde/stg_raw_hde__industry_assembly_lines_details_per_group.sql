with
    source as (

        select *
        from {{ source("raw_hde", "industryassemblylines__details_per_group") }}

    ),

    renamed as (

        select
            time_multiplier,
            cost_multiplier,
            material_multiplier,
            group_id,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id

        from source

    )

select *
from renamed
