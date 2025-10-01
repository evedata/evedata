with
    source as (select * from {{ source("sde_raw", "solar_systems__planets") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as planet_uuid,
            _dlt_parent_id::text as system_uuid,
            id::bigint as planet_id,
            celestial_index::bigint as planet_index,
            planet_attributes__height_map1::bigint as height_map_1_id,
            planet_attributes__height_map2::bigint as height_map_2_id,
            planet_name_id::bigint as name_id,
            type_id::bigint as type_id,
            planet_attributes__shader_preset::bigint as shader_preset_id,

            -- -------- Numerics
            position__x::decimal as position_x,
            position__y::decimal as position_y,
            position__z::decimal as position_z,
            radius::bigint as radius,
            statistics__density::decimal as statistics_density,
            statistics__eccentricity::decimal as statistics_eccentricity,
            statistics__escape_velocity::decimal as statistics_escape_velocity,
            statistics__life::decimal as statistics_life,
            statistics__mass_dust::double as statistics_mass_dust,
            statistics__mass_gas::double as statistics_mass_gas,
            statistics__orbit_period::decimal as statistics_orbit_period,
            statistics__orbit_radius::decimal as statistics_orbit_radius,
            statistics__pressure::decimal as statistics_pressure,
            statistics__radius::decimal as statistics_radius,
            statistics__rotation_rate::decimal as statistics_rotation_rate,
            statistics__spectral_class::text as statistics_spectral_class,
            statistics__surface_gravity::decimal as statistics_surface_gravity,
            statistics__temperature::decimal as statistics_temperature,

            -- -------- Booleans
            planet_attributes__population::boolean as has_population,
            statistics__fragmented::boolean as statistics_is_fragmented,
            statistics__locked::boolean as statistics_is_locked
        from source
    )

select *
from renamed
