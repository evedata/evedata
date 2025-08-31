with
    source as (select * from {{ source("hde_raw", "clone_states__skills") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as clone_state_skill_uuid,
            _dlt_parent_id::text as clone_state_uuid,
            id::bigint as type_id,

            -- -------- Numerics
            value::bigint as level

        from source
    )

select *
from renamed
