with
    source as (select * from {{ source("raw_sde", "map_stargates") }}),

    renamed as (

        select
            _key as stargate_id,
            destination__solar_system_id,
            destination__stargate_id,
            position__x,
            position__y,
            position__z,
            solar_system_id,
            type_id,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
