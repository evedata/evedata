with
    source as (select * from {{ source("raw_sde", "npc_characters") }}),

    renamed as (

        select
            _key as npc_character_id,
            bloodline_id,
            ceo,
            corporation_id,
            gender,
            location_id,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            race_id,
            start_date,
            unique_name,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            ancestry_id,
            career_id,
            school_id,
            speciality_id,
            agent__agent_type_id,
            agent__division_id,
            agent__is_locator,
            agent__level,
            description

        from source

    )

select *
from renamed
