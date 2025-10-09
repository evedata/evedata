with
    source as (select * from {{ source("raw_hde", "expertsystems") }}),

    renamed as (

        select
            _key,
            internal_name,
            es_hidden,
            duration_days,
            es_retired,
            _hde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
