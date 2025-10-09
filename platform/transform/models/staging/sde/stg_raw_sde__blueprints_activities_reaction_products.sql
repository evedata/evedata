with
    source as (

        select *
        from {{ source("raw_sde", "blueprints__activities__reaction__products") }}

    ),

    renamed as (

        select quantity, type_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
