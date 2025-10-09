with
    source as (select * from {{ source("raw_sde", "corporation_activities") }}),

    renamed as (

        select
            _key as corporation_activity_id,
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
