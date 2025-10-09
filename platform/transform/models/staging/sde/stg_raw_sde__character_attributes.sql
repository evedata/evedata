with
    source as (select * from {{ source("raw_sde", "character_attributes") }}),

    renamed as (

        select
            _key as character_attribute_id,
            description,
            icon_id,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            notes,
            short_description,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
