with
    source as (select * from {{ source("raw_sde", "station_operations") }}),

    renamed as (

        select
            _key,
            activity_id,
            border,
            corridor,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            fringe,
            hub,
            manufacturing_factor,
            operation_name__de,
            operation_name__en,
            operation_name__es,
            operation_name__fr,
            operation_name__ja,
            operation_name__ko,
            operation_name__ru,
            operation_name__zh,
            ratio,
            research_factor,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
