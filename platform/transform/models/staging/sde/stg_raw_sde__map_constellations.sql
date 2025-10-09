with
    source as (select * from {{ source("raw_sde", "map_constellations") }}),

    renamed as (

        select
            _key as constellation_id,
            faction_id,
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
            region_id,
            wormhole_class_id,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
