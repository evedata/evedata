with
    source as (select * from {{ source("raw_hde", "schoolmap") }}),

    renamed as (

        select _key, solar_system_id, school_id, _hde_version, _dlt_load_id, _dlt_id

        from source

    )

select *
from renamed
