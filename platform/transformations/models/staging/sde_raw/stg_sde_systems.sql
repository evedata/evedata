with
    source as (select * from {{ source("sde_raw", "solar_systems") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as system_uuid,
            solar_system_id::bigint as system_id,
            constellation_id::bigint as constellation_id,
            description_id::bigint as description_id,
            faction_id::bigint as faction_id,
            solar_system_name_id::bigint as name_id,
            secondary_sun__effect_beacon_type_id::bigint
            as secondary_sun_effect_beacon_type_id,
            secondary_sun__item_id::bigint as secondary_sun_id,
            secondary_sun__type_id::bigint as secondary_sun_type_id,
            star__id::bigint as star_id,
            star__type_id::bigint as star_type_id,
            sun_type_id::bigint as sun_type_id,
            wormhole_class_id::smallint as wormhole_class_id,

            -- -------- Text
            sde_version::text as sde_version,
            security_class::text as security_class,
            star__statistics__spectral_class::text as star_statistics_spectral_class,
            visual_effect::text as visual_effect,

            -- -------- Numerics
            center__x::double as center_x,
            center__y::double as center_y,
            center__z::double as center_z,
            max__x::double as maximum_x,
            max__y::double as maximum_y,
            max__z::double as maximum_z,
            min__x::double as minimum_x,
            min__y::double as minimum_y,
            min__z::double as minimum_z,
            radius::decimal as radius,
            secondary_sun__position__x::double as secondary_sun_position_x,
            secondary_sun__position__y::double as secondary_sun_position_y,
            secondary_sun__position__z::double as secondary_sun_position_z,
            security::decimal as security_status,
            star__radius::bigint as star_radius,
            star__statistics__age::double as star_statistics_age,
            star__statistics__life::double as star_statistics_life,
            luminosity::decimal as statistics_luminosity,
            star__statistics__locked::boolean as star_statistics_is_locked,
            star__statistics__luminosity::decimal as star_statistics_luminosity,
            star__statistics__radius::decimal as star_statistics_radius,
            star__statistics__temperature::decimal as star_statistics_temperature,

            -- -------- Booleans
            fringe::boolean as is_fringe,
            border::boolean as is_border,
            corridor::boolean as is_corridor,
            hub::boolean as is_hub,
            international::boolean as is_international,
            regional::boolean as is_regional

        from source
    )

select *
from renamed
