with
    source as (

        select * from {{ source("raw_sde", "station_operations__station_types") }}

    ),

    renamed as (

        select _key, _value as station_type_id, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
