with
    source as (select * from {{ source("raw_hde", "schools") }}),

    renamed as (

        select
            _key,
            corporation_id,
            career_id,
            race_id,
            title,
            icon_id,
            character_description,
            description,
            _hde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
