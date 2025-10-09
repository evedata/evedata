with
    source as (select * from {{ source("raw_hde", "industryassemblylines") }}),

    renamed as (

        select
            _key,
            base_material_multiplier,
            description,
            base_time_multiplier,
            activity,
            id,
            name,
            _hde_version,
            _dlt_load_id,
            _dlt_id,
            base_cost_multiplier

        from source

    )

select *
from renamed
