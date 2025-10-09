with
    source as (select * from {{ source("raw_sde", "factions") }}),

    renamed as (

        select
            _key as faction_id,
            corporation_id,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            flat_logo,
            flat_logo_with_name,
            icon_id,
            militia_corporation_id,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            short_description__de,
            short_description__en,
            short_description__es,
            short_description__fr,
            short_description__ja,
            short_description__ko,
            short_description__ru,
            short_description__zh,
            size_factor,
            solar_system_id,
            unique_name,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
