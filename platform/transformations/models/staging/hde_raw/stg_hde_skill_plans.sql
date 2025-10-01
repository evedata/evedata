with
    source as (select * from {{ source("hde_raw", "skill_plans") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as skill_plan_uuid,
            id::bigint as skill_plan_id,
            /*
        Career path mappings (derived from analysis of career_path_id to corporation
        division_id relationships):
        * 4 = Explorer (corporation division 26),
        * 5 = Industrialist (corporation divisions 25 & 27: Entrepreneur and Producer),
        * 6 = Enforcer (corporation division 28: Military career),
        * 7 = Soldier of Fortune (corporation division 29: Advanced Military career),
        *
        * These mappings were determined by analyzing the relationship between career
        path_id and corporation_division_id in the skill plans data, then
        cross-referencing with the sde_corporation_divisions table to identify the
        career names.
        */
            career_path_id::bigint as career_path_id,
            npc_corporation_division::bigint as corporation_division_id,
            faction_id::bigint as faction_id,

            -- -------- Text
            description::text as description,
            hde_version::text as hde_version,
            internal_name::text as internal_name,
            name::text as name

        from source
    )

select *
from renamed
