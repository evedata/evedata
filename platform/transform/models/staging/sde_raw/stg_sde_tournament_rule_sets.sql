with
    source as (select * from {{ source("sde_raw", "tournament_rule_sets") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as tournament_rule_set_uuid,
            rule_set_id::text as tournament_rule_set_id,

            -- -------- Text
            rule_set_name::text as name,
            sde_version::text as sde_version,

            -- -------- Numerics
            maximum_pilots_match::bigint as maximum_pilots_match,
            maximum_points_match::bigint as maximum_points_match

        from source
    )

select *
from renamed
