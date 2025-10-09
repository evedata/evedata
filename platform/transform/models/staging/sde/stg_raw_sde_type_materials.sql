with
    source as (select * from {{ source("raw_sde", "type_materials") }}),

    renamed as (select _key, _sde_version, _dlt_load_id, _dlt_id from source)

select *
from renamed
