with
    source as (select * from {{ source("raw_sde", "bloodlines") }}),

    renamed as (

        select
            _key as bloodline_id,
            charisma,
            corporation_id,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            icon_id,
            intelligence,
            memory,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            perception,
            race_id,
            willpower,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
