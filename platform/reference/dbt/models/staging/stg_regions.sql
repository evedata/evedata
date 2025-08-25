WITH source AS (
    SELECT * FROM {{ source('sde', 'regions') }}
)

SELECT
    id,
    name,
    universe,
    center__x AS center_x,
    center__y AS center_y,
    center__z AS center_z,
    min__x AS min_x,
    min__y AS min_y,
    min__z AS min_z,
    max__x AS max_x,
    max__y AS max_y,
    max__z AS max_z,
    faction_id,
    nebula_id,
    wormhole_class_id
FROM source
