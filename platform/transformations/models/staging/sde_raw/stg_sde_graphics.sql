with
    source as (select * from {{ source("sde_raw", "graphics") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as graphic_uuid,
            id::bigint as graphic_id,

            -- -------- Text
            description::text as description,
            graphic_file::text as graphic_file,
            icon_info__folder::text as icon_folder,
            sde_version::text as sde_version,
            sof_faction_name::text as sof_faction_name,
            sof_hull_name::text as sof_hull_name,
            sof_race_name::text as sof_race_name

        from source
    )

select *
from renamed
