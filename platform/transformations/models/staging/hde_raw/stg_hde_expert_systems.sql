with
    source as (select * from {{ source("hde_raw", "expert_systems") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as expert_system_uuid,
            id::bigint as expert_system_id,

            -- -------- Text
            hde_version::text as hde_version,
            internal_name::text as internal_name,

            -- -------- Numerics
            duration_days::bigint as duration_days,

            -- --------- Timestamps
            case
                when es_hidden::smallint = 0
                then false
                when es_hidden::smallint is null
                then false
                else true
            end as is_hidden,
            case
                when es_retired::smallint = 0
                then false
                when es_retired::smallint is null
                then false
                else true
            end as is_retired

        from source
    )

select *
from renamed
