with
    celestials as (select * from {{ ref("int_celestials") }}),
    types as (select * from {{ ref("dim_types") }}),

    joined as (
        select celestials.*, types.type_key
        from celestials
        left join types on celestials.type_id = types.type_id
    )

select *
from joined
