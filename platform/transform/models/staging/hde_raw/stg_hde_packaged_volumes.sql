with
    source as (select * from {{ source("hde_raw", "repackaged_volumes") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as repackaged_volume_uuid,
            key::bigint as type_id,

            -- -------- Text
            hde_version::text as hde_version,

            -- -------- Numerics
            value::decimal as packaged_volume

        from source
    )

select *
from renamed
