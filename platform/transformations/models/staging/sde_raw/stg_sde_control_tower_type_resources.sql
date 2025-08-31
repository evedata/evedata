with
    source as (
        select * from {{ source("sde_raw", "control_tower_resources__resources") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as control_tower_type_resource_uuid,
            _dlt_parent_id::text as control_tower_type_uuid,
            resource_type_id::bigint as resource_type_id,
            faction_id::bigint as faction_id,

            -- -------- Numerics
            purpose::bigint as purpose,
            quantity::bigint as quantity,
            min_security_level::decimal as min_security_level

        from source
    )

select *
from renamed
