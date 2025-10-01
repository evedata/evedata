with
    source as (select * from {{ source("sde_raw", "sovereignty_upgrades") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as sovereignty_upgrade_uuid,
            id::bigint as type_id,
            fuel_type_id::bigint as fuel_type_id,

            -- -------- Text
            mutually_exclusive_group::text as mutually_exclusive_group,
            sde_version::text as sde_version,

            -- -------- Numerics
            fuel_hourly_upkeep::bigint as fuel_hourly_upkeep,
            fuel_startup_cost::bigint as fuel_startup_cost,
            power_allocation::bigint as power_allocation,
            workforce_allocation::bigint as workforce_allocation

        from source
    )

select *
from renamed
