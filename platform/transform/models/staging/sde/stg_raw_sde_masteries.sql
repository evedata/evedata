with
    source as (select * from {{ source("raw_sde", "masteries") }}),

    renamed as (select _key as type_id, _sde_version, _dlt_load_id, _dlt_id from source)

select *
from renamed
