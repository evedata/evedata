with
    source as (

        select *
        from {{ source("raw_hde", "industrymodifiersources__research_time__time") }}

    ),

    renamed as (

        select dogma_attribute_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
