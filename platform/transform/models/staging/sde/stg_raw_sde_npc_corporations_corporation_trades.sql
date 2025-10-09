with
    source as (

        select * from {{ source("raw_sde", "npc_corporations__corporation_trades") }}

    ),

    renamed as (select _key, _value, _dlt_parent_id, _dlt_list_idx, _dlt_id from source)

select *
from renamed
