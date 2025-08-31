with
    asteroid_belts as (select * from {{ ref("stg_sde_asteroid_belts") }}),
    names as (select * from {{ ref("stg_sde_item_names") }}),
    planets as (select * from {{ ref("stg_sde_planets") }}),
    systems as (select * from {{ ref("stg_sde_systems") }}),

    joined as (
        select
            asteroid_belts.asteroid_belt_id,
            planets.planet_id,
            systems.system_id,
            asteroid_belts.type_id,
            names.name,
            asteroid_belts.asteroid_belt_index,
            asteroid_belts.position_x,
            asteroid_belts.position_y,
            asteroid_belts.position_z
        from asteroid_belts
        inner join planets on asteroid_belts.planet_uuid = planets.planet_uuid
        inner join systems on asteroid_belts.system_uuid = systems.system_uuid
        left join names on asteroid_belts.asteroid_belt_id = names.item_id
    )

select *
from joined
