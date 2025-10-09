with
    source as (

        select * from {{ source("raw_hde", "expertsystems__associated_ship_types") }}

    ),

    renamed as (select value, _dlt_parent_id, _dlt_list_idx, _dlt_id from source)

select *
from renamed
