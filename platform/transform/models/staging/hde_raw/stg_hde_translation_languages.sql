with
    source as (select * from {{ source("hde_raw", "localization_languages") }}),

    renamed as (
        select
            -- -------- IDs
            _dlt_id::text as translation_language_uuid,

            -- -------- Text
            value::text as code,
            hde_version::text as hde_version

        from source
    )

select *
from renamed
