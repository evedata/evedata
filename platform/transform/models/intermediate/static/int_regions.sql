with
    names as (select * from {{ ref("stg_sde_item_names") }}),

    regions as (
        select
            {{
                dbt_utils.star(
                    from=ref("stg_sde_regions"),
                    except=["region_uuid", "description_id", "name_id"],
                )
            }}
        from {{ ref("stg_sde_regions") }}
    ),

    joined as (
        select regions.*, names.name
        from regions
        left join names on regions.region_id = names.item_id
    )

select *
from joined
