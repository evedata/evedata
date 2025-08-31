with
    source as (select * from {{ source("sde_raw", "npc_corporations__divisions") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as npc_corporation_division_uuid,
            _dlt_parent_id::text as npc_corporation_uuid,
            id::smallint as npc_corporation_division_type_id,
            leader_id::bigint as leader_id,

            -- -------- Numerics
            division_number::smallint as division_number,
            size::smallint as size

        from source
    )

select *
from renamed
