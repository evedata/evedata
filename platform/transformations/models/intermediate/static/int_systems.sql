with
    names as (select * from {{ ref("stg_sde_item_names") }}),

    systems as (select * from {{ ref("stg_sde_systems") }}),

    systems_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from systems
        window w as (partition by system_id order by sde_version)
    ),

    joined as (
        select
            systems.system_id,
            systems.constellation_id,
            systems.faction_id,
            systems.wormhole_class_id,
            names.name,
            systems.security_class,
            systems.visual_effect,
            systems.center_x,
            systems.center_y,
            systems.center_z,
            systems.maximum_x,
            systems.maximum_y,
            systems.maximum_z,
            systems.minimum_x,
            systems.minimum_y,
            systems.minimum_z,
            systems.radius,
            systems.security_status,
            systems.is_fringe,
            systems.is_border,
            systems.is_corridor,
            systems.is_hub,
            systems.is_international,
            systems.from_sde_version,
            systems.to_sde_version
        from systems_scd2 as systems
        left join names on systems.system_id = names.item_id
    ),

    final as (
        select
            *,

            {{ dbt_utils.generate_surrogate_key(["system_id", "from_sde_version"]) }}
            as system_sk,
            coalesce(to_sde_version is null, false) as is_current
        from joined
    )

select *
from final
