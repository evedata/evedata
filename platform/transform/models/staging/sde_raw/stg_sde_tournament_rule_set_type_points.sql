with
    source as (
        select * from {{ source("sde_raw", "tournament_rule_sets__points__types") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as tournament_rule_set_type_point_uuid,
            _dlt_parent_id::text as tournament_rule_set_uuid,
            type_id::bigint as type_id,

            -- -------- Numerics
            points::bigint as points

        from source
    )

select *
from renamed
