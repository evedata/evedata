with
    source as (select * from {{ source("raw_sde", "masteries___value") }}),

    renamed as (

        select _key as level, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
