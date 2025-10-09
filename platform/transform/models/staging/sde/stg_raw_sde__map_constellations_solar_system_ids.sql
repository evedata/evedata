with
    source as (

        select * from {{ source("raw_sde", "map_constellations__solar_system_ids") }}

    ),

    renamed as (

        select value as solar_system_id, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
