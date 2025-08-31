with
    items as (select * from {{ ref("stg_sde_items") }}),
    names as (select * from {{ ref("stg_sde_item_names") }}),
    positions as (select * from {{ ref("stg_sde_item_positions") }}),
    unique_names as (select * from {{ ref("stg_sde_item_unique_names") }}),

    joined as (
        select
            items.item_id,
            items.flag_id,
            unique_names.group_id,
            items.location_id,
            items.parent_item_id,
            names.name,
            unique_names.unique_name,
            items.quantity,
            positions.pitch as position_pitch,
            positions.roll as position_roll,
            positions.x as position_x,
            positions.y as position_y,
            positions.yaw as position_yaw,
            positions.z as position_z
        from items
        left join names on items.item_id = names.item_id
        left join positions on items.item_id = positions.item_id
        left join unique_names on items.item_id = unique_names.item_id
    )

select *
from joined
