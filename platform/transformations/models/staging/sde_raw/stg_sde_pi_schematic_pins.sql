with
    source as (select * from {{ source("sde_raw", "planet_schematics__pins") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as pi_schematic_pin_uuid,
            _dlt_parent_id::text as pi_schematic_uuid,
            value::bigint as type_id

        from source
    )

select *
from renamed
