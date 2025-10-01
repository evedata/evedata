{{ config(materialized="table") }}

with
    type_reprocessing_output_types as (
        select * from {{ ref("stg_sde_type_reprocessing_output_types") }}
    ),

    type_reprocessing_outputs as (
        select * from {{ ref("stg_sde_type_reprocessing_outputs") }}
    ),
    type_reprocessing_outputs_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from type_reprocessing_outputs
        window w as (partition by type_id order by sde_version)
    ),

    joined as (
        select
            type_reprocessing_outputs.type_id,
            type_reprocessing_output_types.type_id as output_type_id,
            type_reprocessing_output_types.quantity,
            type_reprocessing_outputs.from_sde_version,
            type_reprocessing_outputs.to_sde_version
        from type_reprocessing_output_types
        inner join
            type_reprocessing_outputs_scd2 as type_reprocessing_outputs
            on type_reprocessing_output_types.type_reprocessing_output_uuid
            = type_reprocessing_outputs.type_reprocessing_output_uuid
    ),

    final as (
        select
            *,

            {{ dbt_utils.generate_surrogate_key(["type_id", "output_type_id", "from_sde_version"]) }}
            as type_reprocessing_output_sk,
            coalesce(to_sde_version is null, false) as is_current
        from joined
    )

select *
from final
