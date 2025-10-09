with
    source as (select * from {{ source("raw_sde", "planet_resources") }}),

    renamed as (

        select
            _key as celestial_id,
            power,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            workforce,
            cycle_minutes,
            harvest_silo_max,
            maturation_cycle_minutes,
            maturation_percent,
            mature_silo_max,
            reagent_harvest_amount,
            reagent_type_id

        from source

    )

select *
from renamed
