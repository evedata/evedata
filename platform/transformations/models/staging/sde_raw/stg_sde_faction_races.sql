with
    source as (select * from {{ source("sde_raw", "factions__member_races") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as faction_race_uuid,
            _dlt_parent_id::text as faction_uuid,
            value::bigint as race_id

        from source
    )

select *
from renamed
