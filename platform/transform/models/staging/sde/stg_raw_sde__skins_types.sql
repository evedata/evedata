with
    source as (select * from {{ source("raw_sde", "skins__types") }}),

    renamed as (

        select value as type_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
