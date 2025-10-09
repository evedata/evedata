with
    source as (select * from {{ source("raw_sde", "map_regions") }}),

    renamed as (

        select
            _key as region_id,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            faction_id,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            nebula_id,
            position__x,
            position__y,
            position__z,
            wormhole_class_id,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
