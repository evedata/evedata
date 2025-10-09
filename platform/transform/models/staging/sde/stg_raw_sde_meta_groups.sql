with
    source as (select * from {{ source("raw_sde", "meta_groups") }}),

    renamed as (

        select
            _key as meta_group_id,
            color__b,
            color__g,
            color__r,
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
            _dlt_id,
            icon_id,
            icon_suffix,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh

        from source

    )

select *
from renamed
