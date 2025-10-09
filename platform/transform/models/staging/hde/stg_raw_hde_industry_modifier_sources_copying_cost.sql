with
    source as (

        select * from {{ source("raw_hde", "industrymodifiersources__copying__cost") }}

    ),

    renamed as (

        select dogma_attribute_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
