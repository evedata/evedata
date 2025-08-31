with
    source as (select * from {{ source("sde_raw", "types__traits__types") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as type_bonus_uuid,
            _dlt_parent_id::text as type_uuid,
            _dlt_list_idx::bigint as bonus_index,
            id::bigint as bonus_type_id

        from source
    )

select *
from renamed
