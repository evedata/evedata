with
    source as (select * from {{ source("sde_raw", "agents_in_space") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as agent_in_space_uuid,
            id::bigint as agent_id,
            dungeon_id::bigint as dungeon_id,
            solar_system_id::bigint as system_id,
            spawn_point_id::bigint as spawn_point_id,
            type_id::bigint as ship_type_id,

            -- -------- Text
            sde_version::text as sde_version

        from source
    )

select *
from renamed
