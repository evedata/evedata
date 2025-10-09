with
    source as (select * from {{ source("raw_sde", "map_planets__asteroid_belt_ids") }}),

    renamed as (

        select value as asteroid_belt_id, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
