with
    source as (

        select *
        from {{ source("raw_sde", "dynamic_item_attributes__input_output_mapping") }}

    ),

    renamed as (

        select
            resulting_type as resulting_type_id, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
