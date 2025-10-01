with
    source as (select * from {{ source("hde_raw", "dbuffs") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as buff_uuid,
            id::bigint as buff_id,

            -- -------- Text
            aggregate_mode::text as aggregate_mode,
            developer_description::text as developer_description,
            hde_version::text as hde_version,
            operation_name::text as operation_name,
            show_output_value_in_ui::text as show_output_value_in_ui,

            -- -------- Numerics
            display_name_id::bigint as display_name_id

        from source
    )

select *
from renamed
