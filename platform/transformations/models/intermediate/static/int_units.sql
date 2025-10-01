{{ config(materialized="table") }}

with
    units as (
        select
            unit_id,
            description,
            display_name,
            name
        from {{ ref("stg_hde_units") }}
    ),

    units_scd2 as (
        select
            *,
            sde_version as from_sde_version,
            lead(sde_version) over w as to_sde_version
        from units
        window w as (partition by unit_id order by sde_version)
    ),

    final as (
        select
            *,

            {{ dbt_utils.generate_surrogate_key(["unit_id", "from_sde_version"]) }}
            as unit_sk,
            coalesce(to_sde_version is null, false) as is_current
        from units_scd2
    )

select *
from final
