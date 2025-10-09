with
    source as (

        select * from {{ source("raw_sde", "npc_corporations__allowed_member_races") }}

    ),

    renamed as (

        select value as race_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
