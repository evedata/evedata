with
    source as (select * from {{ source("raw_sde", "types") }}),

    renamed as (

        select
            _key,
            group_id,
            mass,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            portion_size,
            published,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            volume,
            radius,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            graphic_id,
            sound_id,
            icon_id,
            race_id,
            base_price,
            market_group_id,
            capacity,
            meta_group_id,
            variation_parent_type_id,
            faction_id

        from source

    )

select *
from renamed
