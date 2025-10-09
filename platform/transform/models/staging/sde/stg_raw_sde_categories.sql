with
    source as (select * from {{ source("raw_sde", "categories") }}),

    renamed as (

        select
            _key as category_id,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            published,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            icon_id

        from source

    )

select *
from renamed
