with
    int_asteroid_belts as (select * from {{ ref("int_asteroid_belts") }}),
    int_constellations as (select * from {{ ref("int_constellations") }}),
    int_moons as (select * from {{ ref("int_moons") }}),
    int_npc_corporations as (select * from {{ ref("int_npc_corporations") }}),
    int_planets as (select * from {{ ref("int_planets") }}),
    int_regions as (select * from {{ ref("int_regions") }}),
    int_secondary_suns as (select * from {{ ref("int_secondary_suns") }}),
    int_stargates as (select * from {{ ref("int_stargates") }}),
    int_stars as (select * from {{ ref("int_stars") }}),
    int_stations as (select * from {{ ref("int_stations") }}),
    int_systems as (select * from {{ ref("int_systems") }}),

    regions as (
        select
            region_id as celestial_id,
            'region' as celestial_type,
            null::bigint as constellation_id,
            faction_id,
            null::bigint as parent_celestial_id,
            region_id,
            null::bigint as system_id,
            3 as type_id,
            wormhole_class_id,
            coalesce(name, 'Unnamed Region ' || region_id) as name,
            universe_name,
            null::smallint as celestial_index,
            maximum_x,
            maximum_y,
            maximum_z,
            minimum_x,
            minimum_y,
            minimum_z,
            null::text as security_class,
            null::decimal as security_status,
            center_x as x,
            center_y as y,
            center_z as z
        from int_regions
    ),

    constellations as (
        select
            c.constellation_id as celestial_id,
            'constellation' as celestial_type,
            c.constellation_id,
            c.faction_id,
            c.region_id as parent_celestial_id,
            c.region_id,
            null::bigint as system_id,
            c.wormhole_class_id,
            4 as type_id,
            coalesce(c.name, 'Unnamed Constellation ' || c.constellation_id) as name,
            r.universe_name,
            null::smallint as celestial_index,
            c.maximum_x,
            c.maximum_y,
            c.maximum_z,
            c.minimum_x,
            c.minimum_y,
            c.minimum_z,
            null::text as security_class,
            null::decimal as security_status,
            c.center_x as x,
            c.center_y as y,
            c.center_z as z
        from int_constellations as c
        inner join int_regions as r on c.region_id = r.region_id
    ),

    systems as (
        select
            s.system_id as celestial_id,
            'system' as celestial_type,
            c.constellation_id,
            s.faction_id,
            s.constellation_id as parent_celestial_id,
            c.region_id,
            s.system_id,
            5 as type_id,
            s.wormhole_class_id,
            coalesce(s.name, 'Unnamed System ' || s.system_id) as name,
            r.universe_name,
            null::smallint as celestial_index,
            s.maximum_x,
            s.maximum_y,
            s.maximum_z,
            s.minimum_x,
            s.minimum_y,
            s.minimum_z,
            s.security_class,
            s.security_status,
            s.center_x as x,
            s.center_y as y,
            s.center_z as z
        from int_systems as s
        inner join int_constellations as c on s.constellation_id = c.constellation_id
        inner join int_regions as r on c.region_id = r.region_id
    ),

    stars as (
        select
            s.star_id as celestial_id,
            'star' as celestial_type,
            sy.constellation_id,
            sy.faction_id,
            s.system_id as parent_celestial_id,
            r.region_id,
            s.system_id,
            s.type_id,
            sy.wormhole_class_id,
            coalesce(s.name, 'Unnamed Star ' || s.star_id) as name,
            r.universe_name,
            null::smallint as celestial_index,
            null::decimal as maximum_x,
            null::decimal as maximum_y,
            null::decimal as maximum_z,
            null::decimal as minimum_x,
            null::decimal as minimum_y,
            null::decimal as minimum_z,
            sy.security_class,
            sy.security_status,
            0.0::decimal as x,
            0.0::decimal as y,
            0.0::decimal as z
        from int_stars as s
        inner join int_systems as sy on s.system_id = sy.system_id
        inner join int_constellations as c on sy.constellation_id = c.constellation_id
        inner join int_regions as r on c.region_id = r.region_id
    ),

    secondary_suns as (
        select
            s.secondary_sun_id as celestial_id,
            'secondary_sun' as celestial_type,
            c.constellation_id,
            sy.faction_id,
            s.system_id as parent_celestial_id,
            c.region_id,
            s.system_id,
            s.type_id,
            sy.wormhole_class_id,
            coalesce(s.name, 'Unnamed Secondary Sun ' || s.secondary_sun_id) as name,
            r.universe_name,
            null::smallint as celestial_index,
            null::decimal as maximum_x,
            null::decimal as maximum_y,
            null::decimal as maximum_z,
            null::decimal as minimum_x,
            null::decimal as minimum_y,
            null::decimal as minimum_z,
            sy.security_class,
            sy.security_status,
            s.position_x as x,
            s.position_y as y,
            s.position_z as z
        from int_secondary_suns as s
        inner join int_systems as sy on s.system_id = sy.system_id
        inner join int_constellations as c on sy.constellation_id = c.constellation_id
        inner join int_regions as r on c.region_id = r.region_id
    ),

    planets as (
        select
            p.planet_id as celestial_id,
            'planet' as celestial_type,
            c.constellation_id,
            s.faction_id,
            s.system_id as parent_celestial_id,
            r.region_id,
            s.system_id,
            p.type_id,
            s.wormhole_class_id,
            coalesce(p.name, 'Unnamed Planet ' || p.planet_id) as name,
            r.universe_name,
            p.planet_index as celestial_index,
            null::decimal as maximum_x,
            null::decimal as maximum_y,
            null::decimal as maximum_z,
            null::decimal as minimum_x,
            null::decimal as minimum_y,
            null::decimal as minimum_z,
            s.security_class,
            s.security_status,
            p.position_x as x,
            p.position_y as y,
            p.position_z as z
        from int_planets as p
        inner join int_systems as s on p.system_id = s.system_id
        inner join int_constellations as c on s.constellation_id = c.constellation_id
        inner join int_regions as r on c.region_id = r.region_id
    ),

    asteroid_belts as (
        select
            a.asteroid_belt_id as celestial_id,
            'asteroid_belt' as celestial_type,
            c.constellation_id,
            s.faction_id,
            p.planet_id as parent_celestial_id,
            r.region_id,
            s.system_id,
            a.type_id,
            s.wormhole_class_id,
            coalesce(a.name, 'Unnamed Asteroid Belt ' || a.asteroid_belt_id) as name,
            r.universe_name,
            a.asteroid_belt_index as celestial_index,
            null::decimal as maximum_x,
            null::decimal as maximum_y,
            null::decimal as maximum_z,
            null::decimal as minimum_x,
            null::decimal as minimum_y,
            null::decimal as minimum_z,
            s.security_class,
            s.security_status,
            a.position_x as x,
            a.position_y as y,
            a.position_z as z
        from int_asteroid_belts as a
        inner join int_planets as p on a.planet_id = p.planet_id
        inner join int_systems as s on a.system_id = s.system_id
        inner join int_constellations as c on s.constellation_id = c.constellation_id
        inner join int_regions as r on c.region_id = r.region_id
    ),

    moons as (
        select
            m.moon_id as celestial_id,
            'moon' as celestial_type,
            c.constellation_id,
            s.faction_id,
            p.planet_id as parent_celestial_id,
            r.region_id,
            s.system_id,
            m.type_id,
            s.wormhole_class_id,
            coalesce(m.name, 'Unnamed Moon ' || m.moon_id) as name,
            r.universe_name,
            m.moon_index as celestial_index,
            null::decimal as maximum_x,
            null::decimal as maximum_y,
            null::decimal as maximum_z,
            null::decimal as minimum_x,
            null::decimal as minimum_y,
            null::decimal as minimum_z,
            s.security_class,
            s.security_status,
            m.position_x as x,
            m.position_y as y,
            m.position_z as z
        from int_moons as m
        inner join int_planets as p on m.planet_id = p.planet_id
        inner join int_systems as s on m.system_id = s.system_id
        inner join int_constellations as c on s.constellation_id = c.constellation_id
        inner join int_regions as r on c.region_id = r.region_id
    ),

    stargates as (
        select
            s.stargate_id as celestial_id,
            'stargate' as celestial_type,
            c.constellation_id,
            sy.faction_id,
            sy.system_id as parent_celestial_id,
            r.region_id,
            sy.system_id,
            s.type_id,
            sy.wormhole_class_id,
            coalesce(s.name, 'Unnamed Stargate ' || s.stargate_id) as name,
            r.universe_name,
            null::smallint as celestial_index,
            null::decimal as maximum_x,
            null::decimal as maximum_y,
            null::decimal as maximum_z,
            null::decimal as minimum_x,
            null::decimal as minimum_y,
            null::decimal as minimum_z,
            sy.security_class,
            sy.security_status,
            s.position_x as x,
            s.position_y as y,
            s.position_z as z
        from int_stargates as s
        inner join int_systems as sy on s.system_id = sy.system_id
        inner join int_constellations as c on sy.constellation_id = c.constellation_id
        inner join int_regions as r on c.region_id = r.region_id
    ),

    stations as (
        select
            s.station_id as celestial_id,
            'station' as celestial_type,
            c.constellation_id,
            co.faction_id,
            coalesce(m.moon_id, p.planet_id) as parent_celestial_id,
            r.region_id,
            sy.system_id,
            s.type_id,
            sy.wormhole_class_id,
            coalesce(s.name, 'Unnamed Station ' || s.station_id) as name,
            r.universe_name,
            null::smallint as celestial_index,
            null::decimal as maximum_x,
            null::decimal as maximum_y,
            null::decimal as maximum_z,
            null::decimal as minimum_x,
            null::decimal as minimum_y,
            null::decimal as minimum_z,
            sy.security_class,
            sy.security_status,
            s.position_x as x,
            s.position_y as y,
            s.position_z as z
        from int_stations as s
        left join int_moons as m on s.moon_id = m.moon_id
        left join int_planets as p on s.planet_id = p.planet_id
        inner join int_systems as sy on s.system_id = sy.system_id
        inner join int_constellations as c on sy.constellation_id = c.constellation_id
        inner join int_regions as r on c.region_id = r.region_id
        inner join
            int_npc_corporations as co on s.npc_corporation_id = co.npc_corporation_id
    ),

    combined as (
        select *
        from regions
        union
        select *
        from constellations
        union
        select *
        from systems
        union
        select *
        from stars
        union
        select *
        from secondary_suns
        union
        select *
        from planets
        union
        select *
        from asteroid_belts
        union
        select *
        from moons
        union
        select *
        from stargates
        union
        select *
        from stations
    ),

    joined as (
        select
            {{ dbt_utils.generate_surrogate_key(["combined.celestial_id"]) }}
            as celestial_key,
            *,
            case
                when celestial_type in ('region', 'constellation', 'system')
                then 'universe'
                else 'system'
            end as coordinate_system,
            security_status >= 0.5 as is_high_sec,
            security_status < 0.5 and security_status > 0.0 as is_low_sec,
            security_status <= 0.0 as is_null_sec
        from combined
    )

select *
from joined
