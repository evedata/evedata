with
    source as (select * from {{ source("raw_sde", "npc_corporation_divisions") }}),

    renamed as (

        select
            _key as npc_corporation_division_id,
            display_name,
            internal_name,
            leader_type_name__de,
            leader_type_name__en,
            leader_type_name__es,
            leader_type_name__fr,
            leader_type_name__ja,
            leader_type_name__ko,
            leader_type_name__ru,
            leader_type_name__zh,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh

        from source

    )

select *
from renamed
