with
    source as (select * from {{ source("raw_sde", "dogma_units") }}),

    renamed as (

        select
            _key as dogma_unit_id,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            display_name__de,
            display_name__en,
            display_name__es,
            display_name__fr,
            display_name__ja,
            display_name__ko,
            display_name__ru,
            display_name__zh,
            name,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
