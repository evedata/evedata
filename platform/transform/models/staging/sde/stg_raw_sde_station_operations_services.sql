with
    source as (select * from {{ source("raw_sde", "station_operations__services") }}),

    renamed as (

        select value as station_service_id, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
