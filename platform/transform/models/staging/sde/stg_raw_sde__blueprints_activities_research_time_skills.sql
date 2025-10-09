with
    source as (

        select *
        from {{ source("raw_sde", "blueprints__activities__research_time__skills") }}

    ),

    renamed as (

        select level, type_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
