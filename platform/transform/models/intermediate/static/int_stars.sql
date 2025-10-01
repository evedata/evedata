with
    names as (select * from {{ ref("stg_sde_item_names") }}),
    systems as (select * from {{ ref("stg_sde_systems") }} where star_id is not null),

    stars as (
        select
            systems.star_id,
            systems.star_type_id as type_id,
            systems.system_id,
            names.name
        from systems
        left join names on systems.star_id = names.item_id
    )

select *
from stars
