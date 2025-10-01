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

    type_attributes as (select * from {{ ref("stg_sde_type_attributes") }}),

    joined as (
        select
          type_attributes.attribute_id,
          type_dogma.type_id,
          type_attributes.value,
          type_dogma.from_sde_version,
          type_dogma.to_sde_version
        from type_attributes
        inner join
            type_dogma_scd2 as type_dogma on type_attributes.type_dogma_uuid = type_dogma.type_dogma_uuid
    ),

    final as (
        select
            *,

            {{ dbt_utils.generate_surrogate_key(["type_id", "attribute_id", "from_sde_version"]) }}
            as type_attribute_sk,
            coalesce(to_sde_version is null, false) as is_current
        from joined
    )

select *
from final
