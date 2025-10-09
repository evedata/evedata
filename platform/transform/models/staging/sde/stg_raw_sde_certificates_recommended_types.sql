with
    source as (select * from {{ source("raw_sde", "certificates__recommended_for") }}),

    renamed as (

        select value as type_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
