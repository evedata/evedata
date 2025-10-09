with
    source as (select * from {{ source("raw_hde", "schools__starting_stations") }}),

    renamed as (select value, _dlt_parent_id, _dlt_list_idx, _dlt_id from source)

select *
from renamed
