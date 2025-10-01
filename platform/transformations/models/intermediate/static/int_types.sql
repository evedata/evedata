{{ config(materialized="table") }}

with
    types as (
        select
            type_id,
            bonus_icon_id,
            faction_id,
            graphic_id,
            group_id,
            icon_id,
            market_group_id,
            meta_group_id,
            race_id,
            description_en as description,
            name_en as name,
            base_price,
            capacity,
            mass,
            portion_size,
            radius,
            volume,
            sde_version
        from {{ ref("stg_sde_types") }}
    ),

    types_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from types
        window w as (partition by type_id order by sde_version)
    ),

    final as (
        select
            *,

            {{ dbt_utils.generate_surrogate_key(["type_id", "from_sde_version"]) }}
            as type_sk,
            coalesce(to_sde_version is null, false) as is_current
        from types_scd2
    )

select *
from final
