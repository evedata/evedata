with
    source as (select * from {{ source("raw_sde", "map_moons") }}),

    renamed as (

        select
            _key as moon_id,
            attributes__height_map1,
            attributes__height_map2,
            attributes__shader_preset,
            celestial_index,
            orbit_id,
            orbit_index,
            position__x,
            position__y,
            position__z,
            radius,
            solar_system_id,
            statistics__density,
            statistics__eccentricity,
            statistics__escape_velocity,
            statistics__locked,
            statistics__mass_dust,
            statistics__mass_gas,
            statistics__orbit_period,
            statistics__orbit_radius,
            statistics__pressure,
            statistics__rotation_rate,
            statistics__spectral_class,
            statistics__surface_gravity,
            statistics__temperature,
            type_id,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            unique_name__de,
            unique_name__en,
            unique_name__es,
            unique_name__fr,
            unique_name__ja,
            unique_name__ko,
            unique_name__ru,
            unique_name__zh

        from source

    )

select *
from renamed
