with
    source as (select * from {{ source("raw_sde", "blueprints") }}),

    renamed as (

        select
            _key as blueprint_id,
            activities__copying__time,
            activities__manufacturing__time,
            activities__research_material__time,
            activities__research_time__time,
            blueprint_type_id,
            max_production_limit,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            activities__invention__time,
            activities__reaction__time

        from source

    )

select *
from renamed
