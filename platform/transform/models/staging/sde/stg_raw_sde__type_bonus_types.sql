with
    source as (select * from {{ source("raw_sde", "type_bonus__types") }}),

    renamed as (select _key, _dlt_parent_id, _dlt_list_idx, _dlt_id from source)

select *
from renamed
