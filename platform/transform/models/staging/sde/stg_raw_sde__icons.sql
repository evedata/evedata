with
    source as (select * from {{ source("raw_sde", "icons") }}),

    renamed as (

        select _key as icon_id, icon_file, _sde_version, _dlt_load_id, _dlt_id

        from source

    )

select *
from renamed
