with
    source as (select * from {{ source("raw_sde", "graphics__sof_layout") }}),

    renamed as (

        select value as sof_layout_id, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
