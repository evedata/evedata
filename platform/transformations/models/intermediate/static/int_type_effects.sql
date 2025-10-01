{{ config(materialized="table") }}

with
    type_dogma as (select * from {{ ref("stg_sde_type_dogma") }}),

    type_dogma_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from type_dogma
        window w as (partition by type_id order by sde_version)
    ),

    type_effects as (select * from {{ ref("stg_sde_type_effects") }}),

    joined as (
        select
            type_effects.effect_id,
            type_dogma.type_id,
            type_effects.is_default,
            type_dogma.from_sde_version,
            type_dogma.to_sde_version
        from type_effects
        inner join
            type_dogma_scd2 as type_dogma on type_effects.type_dogma_uuid = type_dogma.type_dogma_uuid
    ),

    final as (
        select
            *,

            {{ dbt_utils.generate_surrogate_key(["type_id", "effect_id", "from_sde_version"]) }}
            as type_effect_sk,
            coalesce(to_sde_version is null, false) as is_current
        from joined
    )

select *
from final
