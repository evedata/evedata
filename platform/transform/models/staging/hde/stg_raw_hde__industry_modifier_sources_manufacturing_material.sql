with
    source as (

        select *
        from {{ source("raw_hde", "industrymodifiersources__manufacturing__material") }}

    ),

    renamed as (

        select dogma_attribute_id, _dlt_parent_id, _dlt_list_idx, _dlt_id, filter_id

        from source

    )

select *
from renamed
