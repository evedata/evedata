with
    source as (
        select * from {{ source("sde_raw", "npc_corporations__allowed_member_races") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as npc_corporation_allowed_member_race_uuid,
            _dlt_parent_id::text as npc_corporation_uuid,
            value::bigint as race_id

        from source
    )

select *
from renamed
