with
    source as (select * from {{ source("raw_hde", "skillplans") }}),

    renamed as (

        select
            _key,
            internal_name,
            description,
            career_path_id,
            faction_id,
            name,
            _hde_version,
            _dlt_load_id,
            _dlt_id,
            npc_corporation_division

        from source

    )

select *
from renamed
