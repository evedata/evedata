with
    names as (select * from {{ ref("stg_sde_item_names") }}),
    planets as (select * from {{ ref("stg_sde_planets") }}),
    systems as (select * from {{ ref("stg_sde_systems") }}),

    joined as (
        select
            planets.planet_id,
            systems.system_id,
            planets.type_id,
            names.name,
            planets.planet_index,
            planets.position_x,
            planets.position_y,
            planets.position_z
        from planets
        inner join systems on planets.system_uuid = systems.system_uuid
        left join names on planets.planet_id = names.item_id
    )

select *
from joined
