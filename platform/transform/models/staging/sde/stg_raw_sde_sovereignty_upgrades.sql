with
    source as (select * from {{ source("raw_sde", "sovereignty_upgrades") }}),

    renamed as (

        select
            _key as sovereignty_upgrade_type_id,
            fuel_hourly_upkeep,
            fuel_startup_cost,
            fuel_type_id,
            mutually_exclusive_group,
            power_allocation,
            workforce_allocation,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
