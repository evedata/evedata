with
    source as (select * from {{ source("raw_hde", "clonestates") }}),

    renamed as (

        select _key, internal_description, _hde_version, _dlt_load_id, _dlt_id

        from source

    )

select *
from renamed
