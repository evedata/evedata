with
    source as (

        select * from {{ source("raw_sde", "dbuff_collections__location_modifiers") }}

    ),

    renamed as (

        select dogma_attribute_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
