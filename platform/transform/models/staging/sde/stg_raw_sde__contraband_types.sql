with
    source as (select * from {{ source("raw_sde", "contraband_types") }}),

    renamed as (

        select _key as contraband_type_id, _sde_version, _dlt_load_id, _dlt_id

        from source

    )

select *
from renamed
