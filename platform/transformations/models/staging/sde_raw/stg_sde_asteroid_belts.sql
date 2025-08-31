with
    source as (
        select * from {{ source("sde_raw", "solar_systems__planets__asteroid_belts") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as asteroid_belt_uuid,
            _dlt_parent_id::text as planet_uuid,
            _dlt_root_id::text as system_uuid,
            id::bigint as asteroid_belt_id,
            type_id::bigint as type_id,
            asteroid_belt_name_id::bigint as name_id,

            -- -------- Text
            statistics__spectral_class::text as statistics_spectral_class,

            -- -------- Numerics
            celestial_index::bigint as asteroid_belt_index,
            position__x::decimal as position_x,
            position__y::decimal as position_y,
            position__z::decimal as position_z,
            statistics__density::decimal as statistics_density,
            statistics__eccentricity::decimal as statistics_eccentricity,
            statistics__escape_velocity::decimal as statistics_escape_velocity,
            statistics__life::decimal as statistics_life,
            statistics__mass_dust::decimal as statistics_mass_dust,
            statistics__mass_gas::decimal as statistics_mass_gas,
            statistics__orbit_period::decimal as statistics_orbit_period,
            statistics__orbit_radius::decimal as statistics_orbit_radius,
            statistics__pressure::decimal as statistics_pressure,
            statistics__radius::decimal as statistics_radius,
            statistics__rotation_rate::decimal as statistics_rotation_rate,
            statistics__surface_gravity::decimal as statistics_surface_gravity,
            statistics__temperature::decimal as statistics_temperature,

            -- -------- Booleans
            statistics__fragmented::boolean as statistics_is_fragmented,
            statistics__locked::boolean as statistics_is_locked

        from source
    )

select *
from renamed
