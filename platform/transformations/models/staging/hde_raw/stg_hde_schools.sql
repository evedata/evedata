with
    source as (select * from {{ source("hde_raw", "schools") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as school_uuid,
            id::bigint as school_id,
            career_id::bigint as career_id,
            corporation_id::bigint as corporation_id,
            icon_id::bigint as icon_id,
            race_id::bigint as race_id,

            -- -------- Text
            character_description::text as character_description,
            description::text as description,
            hde_version::text as hde_version,
            title::text as title

        from source
    )

select *
from renamed
