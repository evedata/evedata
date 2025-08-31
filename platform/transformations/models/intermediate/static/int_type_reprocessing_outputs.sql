with
    type_reprocessing_output_types as (
        select * from {{ ref("stg_sde_type_reprocessing_output_types") }}
    ),
    type_reprocessing_outputs as (
        select * from {{ ref("stg_sde_type_reprocessing_outputs") }}
    ),

    joined as (
        select
            type_reprocessing_outputs.type_id,
            type_reprocessing_output_types.type_id as output_type_id,
            type_reprocessing_output_types.quantity
        from type_reprocessing_output_types
        inner join
            type_reprocessing_outputs
            on type_reprocessing_output_types.type_reprocessing_output_uuid
            = type_reprocessing_outputs.type_reprocessing_output_uuid
    )

select *
from joined
