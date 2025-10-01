with
    source as (select * from {{ source("sde_raw", "contraband_types__factions") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as contraband_type_faction_uuid,
            _dlt_parent_id::text as contraband_type_uuid,
            id::bigint as faction_id,

            -- -------- Numerics
            attack_min_sec::decimal as attack_min_sec,
            confiscate_min_sec::decimal as confiscate_min_sec,
            fine_by_value::decimal as fine_by_value,
            standing_loss::decimal as standing_loss

        from source
    )

select *
from renamed
