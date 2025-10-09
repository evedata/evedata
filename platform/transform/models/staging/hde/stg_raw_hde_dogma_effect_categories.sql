with
    source as (select * from {{ source("raw_hde", "dogmaeffectcategories") }}),

    renamed as (select key, value, _hde_version, _dlt_load_id, _dlt_id from source)

select *
from renamed
