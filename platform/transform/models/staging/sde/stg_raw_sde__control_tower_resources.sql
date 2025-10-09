with
    source as (select * from {{ source("raw_sde", "control_tower_resources") }}),

    renamed as (

        select _key as control_tower_type_id, _sde_version, _dlt_load_id, _dlt_id

        from source

    )

select *
from renamed
