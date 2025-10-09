with
    source as (select * from {{ source("raw_sde", "station_services") }}),

    renamed as (

        select
            _key,
            service_name__de,
            service_name__en,
            service_name__es,
            service_name__fr,
            service_name__ja,
            service_name__ko,
            service_name__ru,
            service_name__zh,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh

        from source

    )

select *
from renamed
