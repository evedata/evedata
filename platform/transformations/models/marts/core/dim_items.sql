with
    items as (select * from {{ ref("int_items") }}),
    types as (select * from {{ ref("dim_types") }}),

    joined as (
      select
          items.*,
          {{ dbt_utils.generate_surrogate_key(["items.item_id"]) }} as item_key,
          types.type_key
      from items
      left join types on items.type_id = types.type_id
    )

select *
from joined
