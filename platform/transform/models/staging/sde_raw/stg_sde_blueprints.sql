with
    source as (select * from {{ source("sde_raw", "blueprints") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as blueprint_uuid,
            id::bigint as type_id,

            -- -------- Numerics
            activities__copying__time::bigint as copying_duration_seconds,
            activities__invention__time::bigint as invention_duration_seconds,
            activities__manufacturing__time::bigint as manufacturing_duration_seconds,
            max_production_limit::bigint as max_production_limit,
            activities__reaction__time::bigint as reaction_duration_seconds,
            activities__research_material__time::bigint
            as research_material_duration_seconds,
            activities__research_time__time::bigint as research_time_duration_seconds,
            sde_version::text as sde_version

        from source
    )

select *
from renamed
