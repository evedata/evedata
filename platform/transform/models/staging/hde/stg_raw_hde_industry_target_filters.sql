with
    source as (select * from {{ source("raw_hde", "industrytargetfilters") }}),

    renamed as (select _key, name, _hde_version, _dlt_load_id, _dlt_id from source)

select *
from renamed
