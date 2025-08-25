WITH
sde_stations AS (
    SELECT * FROM {{ source('sde', 'stations') }}
),

sde_system_stations AS (
    SELECT * FROM {{ source('sde', 'solar_systems__stations') }}
)

SELECT
    fsd.id,
    bsd.region_id,
    bsd.constellation_id,
    fsd.solar_system_id,
    fsd.planet_id,
    fsd.moon_id,
    fsd.type_id,
    fsd.graphic_id,
    fsd.operation_id,
    fsd.owner_id,
    fsd.reprocessing_hangar_flag AS reprocessing_hangar_flag_id,
    fsd.reprocessing_efficiency,
    fsd.reprocessing_stations_take,
    bsd.docking_cost_per_volume,
    bsd.max_ship_volume_dockable,
    bsd.office_rental_cost,
    bsd.security,
    fsd.position__x AS position_x,
    fsd.position__y AS position_y,
    fsd.position__z AS position_z,
    fsd.is_conquerable,
    fsd.use_operation_name
FROM sde_system_stations AS fsd
LEFT JOIN sde_stations AS bsd ON fsd.id = bsd.id
