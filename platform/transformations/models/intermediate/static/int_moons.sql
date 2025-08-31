with
    moons as (select * from {{ ref("stg_sde_moons") }}),
    names as (select * from {{ ref("stg_sde_item_names") }}),
    planets as (select * from {{ ref("stg_sde_planets") }}),
    systems as (select * from {{ ref("stg_sde_systems") }}),

    joined as (
        select
            moons.moon_id,
            planets.planet_id,
            systems.system_id,
            moons.type_id,
            names.name,
            moons.moon_index,
            moons.position_x,
            moons.position_y,
            moons.position_z
        from moons
        inner join planets on moons.planet_uuid = planets.planet_uuid
        inner join systems on moons.system_uuid = systems.system_uuid
        left join names on moons.moon_id = names.item_id
    )

select *
from joined
