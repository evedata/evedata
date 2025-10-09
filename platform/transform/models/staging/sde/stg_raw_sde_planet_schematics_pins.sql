with
    source as (select * from {{ source("raw_sde", "planet_schematics__pins") }}),

    renamed as (

        select value as pin_type_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
