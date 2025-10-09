with
    source as (select * from {{ source("raw_sde", "contraband_types__factions") }}),

    renamed as (

        select
            _key as faction_id,
            attack_min_sec,
            confiscate_min_sec,
            fine_by_value,
            standing_loss,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id

        from source

    )

select *
from renamed
