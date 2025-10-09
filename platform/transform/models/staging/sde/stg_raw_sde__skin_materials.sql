with
    source as (select * from {{ source("raw_sde", "skin_materials") }}),

    renamed as (

        select
            _key as skin_material_id,
            display_name__de,
            display_name__en,
            display_name__es,
            display_name__fr,
            display_name__ja,
            display_name__ko,
            display_name__ru,
            display_name__zh,
            material_set_id,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
