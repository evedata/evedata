with
    source as (select * from {{ source("raw_hde", "industryactivities") }}),

    renamed as (

        select
            _key,
            activity_id,
            description,
            activity_name,
            _hde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
