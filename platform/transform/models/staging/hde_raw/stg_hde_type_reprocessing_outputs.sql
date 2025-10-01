with
    source as (select * from {{ source("hde_raw", "type_materials") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_reprocessing_output_uuid,
            id::bigint as type_id,

            -- -------- Text
            hde_version::text as hde_version

        from source
    )

select *
from renamed
