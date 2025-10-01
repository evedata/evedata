with
    names as (select * from {{ ref("stg_sde_item_names") }}),
    systems as (
        select * from {{ ref("stg_sde_systems") }} where secondary_sun_id is not null
    ),

    secondary_suns as (
        select
            systems.secondary_sun_id,
            systems.secondary_sun_effect_beacon_type_id as effect_beacon_type_id,
            systems.secondary_sun_type_id as type_id,
            systems.system_id,
            names.name,
            systems.secondary_sun_position_x as position_x,
            systems.secondary_sun_position_y as position_y,
            systems.secondary_sun_position_z as position_z
        from systems
        left join names on systems.secondary_sun_id = names.item_id
    )

select *
from secondary_suns
