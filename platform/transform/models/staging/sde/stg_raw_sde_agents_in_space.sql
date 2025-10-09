with
    source as (select * from {{ source("raw_sde", "agents_in_space") }}),

    renamed as (

        select
            _key as agent_in_space_id,
            dungeon_id,
            solar_system_id,
            spawn_point_id,
            type_id,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
