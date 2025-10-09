with
    source as (

        select * from {{ source("raw_sde", "npc_corporations__lp_offer_tables") }}

    ),

    renamed as (select value, _dlt_parent_id, _dlt_list_idx, _dlt_id from source)

select *
from renamed
