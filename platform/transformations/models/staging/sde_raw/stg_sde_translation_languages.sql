with
    source as (select * from {{ source("sde_raw", "translation_languages") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as translation_language_uuid,

            -- -------- Text
            key::text as code,
            value::text as name,
            sde_version::text as sde_version

        from source
    )

select *
from renamed
