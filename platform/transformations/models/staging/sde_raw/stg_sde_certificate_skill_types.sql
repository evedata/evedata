with
    source as (select * from {{ source("sde_raw", "certificates__skill_types") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as certificate_skill_uuid,
            _dlt_parent_id::text as certificate_uuid,
            id::bigint as type_id,

            -- -------- Numerics
            advanced::bigint as advanced,
            basic::bigint as basic,
            elite::bigint as elite,
            improved::bigint as improved,
            standard::bigint as standard

        from source
    )

select *
from renamed
