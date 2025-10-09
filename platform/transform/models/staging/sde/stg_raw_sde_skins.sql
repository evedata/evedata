with
    source as (select * from {{ source("raw_sde", "skins") }}),

    renamed as (

        select
            _key as skin_id,
            allow_ccp_devs,
            internal_name,
            skin_material_id,
            visible_serenity,
            visible_tranquility,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            is_structure_skin,
            skin_description__de,
            skin_description__en,
            skin_description__es,
            skin_description__fr,
            skin_description__ja,
            skin_description__ko,
            skin_description__ru,
            skin_description__zh

        from source

    )

select *
from renamed
