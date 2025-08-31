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
            volume
        from {{ ref("stg_sde_types") }}
    )

select *
from types
