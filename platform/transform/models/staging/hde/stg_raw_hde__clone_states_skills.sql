with
    source as (select * from {{ source("raw_hde", "clonestates__skills") }}),

    renamed as (select _key, value, _dlt_parent_id, _dlt_list_idx, _dlt_id from source)

select *
from renamed
