with
    categories as (select * from {{ ref("stg_sde_categories") }}),
    compressible_types as (select * from {{ ref("stg_sde_compressible_types") }}),
    groups as (select * from {{ ref("stg_sde_groups") }}),
    icons as (select * from {{ ref("stg_sde_icons") }}),
    market_groups as (select * from {{ ref("stg_sde_market_groups") }}),
    meta_groups as (select * from {{ ref("stg_sde_meta_groups") }}),
    types as (select * from {{ ref("int_types") }}),
    packaged_volumes as (select * from {{ ref("stg_hde_packaged_volumes") }}),

    joined as (
        select
            types.*,

            {{ dbt_utils.generate_surrogate_key(["types.type_id"]) }} as type_key,
            compressed_types.type_id as compressed_type_id,

            categories.name as category_name,
            groups.name as group_name,
            market_groups.name as market_group_name,
            meta_groups.icon_suffix as meta_group_icon_suffix,
            meta_groups.name as meta_group_name,

            compressed_types.volume as compressed_volume,
            packaged_volumes.packaged_volume,

            '#' || lpad(to_hex(meta_groups.color_r::integer), 2, '0')
                || lpad(to_hex(meta_groups.color_g::integer), 2, '0')
                || lpad(to_hex(meta_groups.color_b::integer), 2, '0')
                || lpad(to_hex(meta_groups.color_a::integer), 2, '0')
                as meta_group_color_rgba_hex
        from types
        left join groups on types.group_id = groups.group_id
        left join categories on groups.category_id = categories.category_id
        left join market_groups on types.market_group_id = market_groups.market_group_id
        left join meta_groups on types.meta_group_id = meta_groups.meta_group_id
        left join compressible_types on types.type_id = compressible_types.type_id
        left join compressed_types as ct on types.type_id = ct.type_id
        left join packaged_volumes on types.type_id = packaged_volumes.type_id
    )

select *
from joined
