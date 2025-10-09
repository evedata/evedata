with
    source as (select * from {{ source("raw_sde", "dogma_effects") }}),

    renamed as (

        select
            _key as dogma_effect_id,
            disallow_auto_repeat,
            discharge_attribute_id,
            duration_attribute_id,
            effect_category_id,
            electronic_chance,
            guid,
            is_assistance,
            is_offensive,
            is_warp_safe,
            name,
            propulsion_chance,
            published,
            range_chance,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            distribution,
            falloff_attribute_id,
            range_attribute_id,
            tracking_speed_attribute_id,
            description__de,
            description__en,
            description__es,
            description__fr,
            description__ja,
            description__ko,
            description__ru,
            description__zh,
            display_name__de,
            display_name__en,
            display_name__es,
            display_name__fr,
            display_name__ja,
            display_name__ko,
            display_name__ru,
            display_name__zh,
            icon_id,
            npc_usage_chance_attribute_id,
            npc_activation_chance_attribute_id,
            fitting_usage_chance_attribute_id,
            resistance_attribute_id

        from source

    )

select *
from renamed
