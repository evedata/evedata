with
    names as (select * from {{ ref("stg_sde_item_names") }}),
    regions as (select * from {{ ref("stg_sde_regions") }}),
    systems as (select * from {{ ref("stg_sde_systems") }}),

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
            systems.is_international
        from systems
        inner join regions on systems.region_id = regions.region_id
        left join names on systems.system_id = names.item_id
    )

select *
from joined
