with
    source as (select * from {{ source("raw_sde", "type_dogma__dogma_attributes") }}),

    renamed as (

        select attribute_id, value, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
