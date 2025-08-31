with
    constellations as (select * from {{ ref("stg_sde_constellations") }}),
    names as (select * from {{ ref("stg_sde_item_names") }}),

    joined as (
        select
            constellations.constellation_id,
            constellations.faction_id,
            constellations.region_id,
            constellations.wormhole_class_id,
            names.name,
            constellations.center_x,
            constellations.center_y,
            constellations.center_z,
            constellations.maximum_x,
            constellations.maximum_y,
            constellations.maximum_z,
            constellations.minimum_x,
            constellations.minimum_y,
            constellations.minimum_z
        from constellations
        left join names on constellations.constellation_id = names.item_id
    )

select *
from joined
