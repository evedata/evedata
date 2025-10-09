with
    source as (select * from {{ source("raw_sde", "certificates") }}),

    renamed as (

        select
            _key as certificate_id,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            group_id,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
