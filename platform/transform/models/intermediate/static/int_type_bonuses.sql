{{ config(materialized="table") }}

with
    misc_bonuses as (select * from {{ ref("stg_sde_type_misc_bonuses") }}),
    role_bonuses as (select * from {{ ref("stg_sde_type_role_bonuses") }}),
    type_bonuses as (select * from {{ ref("stg_sde_type_type_bonuses") }}),
    type_bonus_details as (select * from {{ ref("stg_sde_type_type_bonus_details") }}),
    types as (select sde_version, type_id, type_uuid from {{ ref("stg_sde_types") }}),

    types_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from types
        window w as (partition by type_id order by sde_version)
    ),

    combined as (
        select
            types.type_id,
            null::bigint as bonus_type_id,
            bonuses.unit_id,
            'misc' as bonus_type,
            bonuses.bonus,
            bonuses.bonus_index,
            bonuses.importance,
            bonuses.is_positive,
            types.from_sde_version,
            types.to_sde_version
        from misc_bonuses as bonuses
        inner join types_scd2 as types on bonuses.type_uuid = types.type_uuid

        union

        select
            types.type_id,
            null::bigint as bonus_type_id,
            bonuses.unit_id,
            'role' as bonus_type,
            bonuses.bonus,
            bonuses.bonus_index,
            bonuses.importance,
            null::boolean as is_positive,
            types.from_sde_version,
            types.to_sde_version
        from role_bonuses as bonuses
        inner join types_scd2 as types on bonuses.type_uuid = types.type_uuid

        union all

        select
            types.type_id,
            bonuses.bonus_type_id,
            details.unit_id,
            'type' as bonus_type,
            details.bonus,
            details.bonus_index,
            details.importance,
            null::boolean as is_positive,
            types.from_sde_version,
            types.to_sde_version
        from type_bonus_details as details
        inner join
            type_bonuses as bonuses on details.type_bonus_uuid = bonuses.type_bonus_uuid
        inner join types_scd2 as types on bonuses.type_uuid = types.type_uuid
    ),

    final as (
        select
            *,

            {{ dbt_utils.generate_surrogate_key(["type_id", "bonus_type", "bonus_index", "from_sde_version"]) }}
            as type_bonus_sk,
            coalesce(to_sde_version is null, false) as is_current
        from combined
    )

select *
from final
