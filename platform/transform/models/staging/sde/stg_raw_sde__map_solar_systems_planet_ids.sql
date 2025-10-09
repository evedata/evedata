with
    source as (select * from {{ source("raw_sde", "map_solar_systems__planet_ids") }}),

    renamed as (

        select value as planet_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
