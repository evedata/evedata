with
    source as (select * from {{ source("raw_sde", "graphics") }}),

    renamed as (

        select
            _key as graphic_id,
            graphic_file,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            icon_folder,
            sof_faction_name,
            sof_hull_name,
            sof_race_name,
            sof_material_set_id

        from source

    )

select *
from renamed
