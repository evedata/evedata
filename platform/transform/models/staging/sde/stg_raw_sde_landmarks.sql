with
    source as (select * from {{ source("raw_sde", "landmarks") }}),

    renamed as (

        select
            _key as landmark_id,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            position__x,
            position__y,
            position__z,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            icon_id,
            location_id

        from source

    )

select *
from renamed
