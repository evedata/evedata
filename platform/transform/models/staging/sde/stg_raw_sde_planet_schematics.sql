with
    source as (select * from {{ source("raw_sde", "planet_schematics") }}),

    renamed as (

        select
            _key as planet_schematic_id,
            cycle_time,
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
