with
    source as (

        select * from {{ source("raw_sde", "dynamic_item_attributes__attribute_ids") }}

    ),

    renamed as (

        select
            _key as dogma_attribute_id,
            max,
            min,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id,
            high_is_good

        from source

    )

select *
from renamed
