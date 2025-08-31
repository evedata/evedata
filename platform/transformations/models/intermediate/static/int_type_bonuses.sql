with
    misc_bonuses as (select * from {{ ref("stg_sde_type_misc_bonuses") }}),
    role_bonuses as (select * from {{ ref("stg_sde_type_role_bonuses") }}),
    type_bonuses as (select * from {{ ref("stg_sde_type_type_bonuses") }}),
    type_bonus_details as (select * from {{ ref("stg_sde_type_type_bonus_details") }}),
    types as (select type_id from {{ ref("stg_sde_types") }}),

    combined as (
        select
            types.type_id,
            null::bigint as bonus_type_id,
            bonuses.unit_id,
            'misc' as bonus_type,
            bonuses.bonus,
            bonuses.bonus_index,
            bonuses.importance,
            bonuses.is_positive
        from misc_bonuses as bonuses
        inner join types on bonuses.type_uuid = types.type_uuid

        union

        select
            types.type_id,
            null::bigint as bonus_type_id,
            bonuses.unit_id,
            'role' as bonus_type,
            bonuses.bonus,
            bonuses.bonus_index,
            bonuses.importance,
            null::boolean as is_positive
        from role_bonuses as bonuses
        inner join types on bonuses.type_uuid = types.type_uuid

        union all

        select
            types.type_id,
            bonuses.bonus_type_id,
            details.unit_id,
            'type' as bonus_type,
            details.bonus,
            details.bonus_index,
            details.importance,
            null::boolean as is_positive
        from type_bonus_details as details
        inner join
            type_bonuses as bonuses on details.type_bonus_uuid = bonuses.type_bonus_uuid
        inner join types on bonuses.type_uuid = types.type_uuid
    )

select *
from combined
