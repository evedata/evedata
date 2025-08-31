with
    source as (select * from {{ source("sde_raw", "agents") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as agent_uuid,
            id::bigint as agent_id,
            agent_type_id::smallint as agent_type_id,
            division_id::bigint as npc_corporation_division_id,
            corporation_id::bigint as npc_corporation_id,
            location_id::bigint as station_id,

            -- -------- Numerics
            level::smallint as level,

            -- -------- Booleans
            is_locator::boolean as is_locator

        from source
    )

select *
from renamed
