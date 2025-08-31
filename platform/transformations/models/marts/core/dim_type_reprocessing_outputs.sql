with
    type_reprocessing_outputs as (
        select * from {{ ref("int_type_reprocessing_outputs") }}
    ),
    types as (select * from {{ ref("dim_types") }}),

    joined as (
        select
            type_reprocessing_outputs.*,
            types.type_key,
            output_types.type_key as output_type_key
        from type_reprocessing_outputs
        left join types on type_reprocessing_outputs.type_id = types.type_id
        left join
            types as output_types
            on type_reprocessing_outputs.output_type_id = output_types.type_id
    )

select *
from joined
