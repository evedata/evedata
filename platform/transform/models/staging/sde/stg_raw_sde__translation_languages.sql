with
    source as (select * from {{ source("raw_sde", "translation_languages") }}),

    renamed as (select _key, name, _sde_version, _dlt_load_id, _dlt_id from source)

select *
from renamed
