with
    source as (select * from {{ source("raw_sde", "npc_corporations__divisions") }}),

    renamed as (

        select
            _key as npc_corporation_division_id,
            division_number,
            leader_id,
            size,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id

        from source

    )

select *
from renamed
