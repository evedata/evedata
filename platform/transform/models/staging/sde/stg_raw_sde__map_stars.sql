with
    source as (select * from {{ source("raw_sde", "map_stars") }}),

    renamed as (

        select
            _key as star_id,
            radius,
            solar_system_id,
            statistics__age,
            statistics__life,
            statistics__luminosity,
            statistics__spectral_class,
            statistics__temperature,
            type_id,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
