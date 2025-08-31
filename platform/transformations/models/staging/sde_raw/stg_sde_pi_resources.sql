with
    source as (select * from {{ source("sde_raw", "planet_resources") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as planet_resource_uuid,
            id::bigint as celestial_id,
            reagent_type_id::bigint as reagent_type_id,

            -- -------- Numerics
            cycle_minutes::bigint as cycle_minutes,
            harvest_silo_max::bigint as harvest_silo_max,
            maturation_cycle_minutes::bigint as maturation_cycle_minutes,
            maturation_percent::bigint as maturation_percent,
            mature_silo_max::decimal as mature_silo_max,
            power::bigint as power,
            reagent_harvest_amount::bigint as reagent_harvest_amount,
            workforce::bigint as workforce  -- TODO: confirm if ID

        from source
    )

select *
from renamed
