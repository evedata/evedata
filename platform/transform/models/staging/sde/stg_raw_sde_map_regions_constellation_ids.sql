with
    source as (select * from {{ source("raw_sde", "map_regions__constellation_ids") }}),

    renamed as (

        select value as constellation_id, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
