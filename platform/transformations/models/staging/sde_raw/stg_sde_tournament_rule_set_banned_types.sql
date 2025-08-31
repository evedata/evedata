with
    source as (
        select * from {{ source("sde_raw", "tournament_rule_sets__banned__types") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as tournament_rule_set_banned_type_uuid,
            _dlt_parent_id::text as tournament_rule_set_uuid,
            value::bigint as type_id

        from source
    )

select *
from renamed
