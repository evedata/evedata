with
    source as (select * from {{ source("raw_sde", "map_solar_systems") }}),

    renamed as (

        select
            _key as solar_system_id,
            border,
            constellation_id,
            hub,
            international,
            luminosity,
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
            radius,
            region_id,
            regional,
            security_class,
            security_status,
            star_id,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            corridor,
            fringe,
            wormhole_class_id,
            visual_effect,
            faction_id

        from source

    )

select *
from renamed
