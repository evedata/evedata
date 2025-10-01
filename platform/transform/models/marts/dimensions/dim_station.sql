with current_stations as (
    select
        {{ dbt_utils.star(from=ref("dim_station_scd2"), except=["is_current", "from_sde_version", "to_sde_version"]) }}
    from {{ ref("dim_station_scd2") }}
    where is_current = true
)

select *
from current_stations
