with
    source as (select * from {{ source("raw_sde", "agent_types") }}),

    renamed as (

        select _key as agent_type_id, name, _sde_version, _dlt_load_id, _dlt_id

        from source

    )

select *
from renamed
