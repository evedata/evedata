with
    source as (select * from {{ source("hde_raw", "compressible_types") }}),

    renamed as (
        select

            -- -------- IDs
            {{ dbt_utils.generate_surrogate_key(["key", "value"]) }}
            as compressible_type_uuid,  -- noqa: LT05
            key::bigint as type_id,
            value::bigint as compressed_type_id,

            -- -------- Text
            hde_version::text as hde_version

        from source
    )

select *
from renamed
