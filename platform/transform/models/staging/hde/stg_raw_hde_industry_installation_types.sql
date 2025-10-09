with
    source as (select * from {{ source("raw_hde", "industryinstallationtypes") }}),

    renamed as (select _key, type_id, _hde_version, _dlt_load_id, _dlt_id from source)

select *
from renamed
