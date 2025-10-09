with
    source as (

        select *
        from {{ source("raw_hde", "industryassemblylines__details_per_type_list") }}

    ),

    renamed as (

        select
            time_multiplier,
            type_list_id,
            material_multiplier,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id

        from source

    )

select *
from renamed
