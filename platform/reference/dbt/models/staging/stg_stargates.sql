WITH source AS (
    SELECT * FROM {{ source('sde', 'solar_systems__stargates') }}
)

SELECT
    id,

    destination_id,
    solar_system_id,
    type_id,

    name,
    position__x AS position_x,
    position__y AS position_y,
    position__z AS position_z
FROM source
