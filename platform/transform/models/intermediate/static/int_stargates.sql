with
    names as (select * from {{ ref("stg_sde_item_names") }}),
    stargates as (select * from {{ ref("stg_sde_stargates") }}),
    systems as (select * from {{ ref("stg_sde_systems") }}),

    joined as (
        select
            stargates.stargate_id,
            stargates.destination_stargate_id,
            systems.system_id,
            stargates.type_id,
            names.name,
            stargates.position_x,
            stargates.position_y,
            stargates.position_z
        from stargates
        inner join systems on stargates.system_uuid = systems.system_uuid
        left join names on stargates.stargate_id = names.item_id
    )

select *
from joined
