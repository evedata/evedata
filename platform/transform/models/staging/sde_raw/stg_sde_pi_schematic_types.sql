with
    source as (select * from {{ source("sde_raw", "planet_schematics__types") }}),

    renamed as (
        select
            _dlt_id::text as pi_schematic_type_uuid,
            _dlt_parent_id::text as pi_schematic_uuid,
            id::bigint as type_id,
            is_input::boolean as is_input,
            quantity::bigint as quantity

        from source
    )

select *
from renamed
