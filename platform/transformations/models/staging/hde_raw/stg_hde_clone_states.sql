with
    source as (select * from {{ source("hde_raw", "clone_states") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as clone_state_uuid,
            id::bigint as clone_state_id,

            -- -------- Text
            internal_description::text as internal_description

        from source
    )

select *
from renamed
