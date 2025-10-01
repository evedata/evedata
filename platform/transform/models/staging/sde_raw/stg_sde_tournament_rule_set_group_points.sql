with
    source as (
        select * from {{ source("sde_raw", "tournament_rule_sets__points__groups") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as tournament_rule_set_group_point_uuid,
            _dlt_parent_id::text as tournament_rule_set_uuid,
            group_id::bigint as group_id,

            -- -------- Numerics
            points::bigint as points

        from source
    )

select *
from renamed
