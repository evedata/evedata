with
    source as (select * from {{ source("hde_raw", "agent_types") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as agent_type_uuid,
            key::smallint as agent_type_id,

            -- -------- Text
            hde_version::text as hde_version,
            value::text as name

        from source
    )

select *
from renamed
