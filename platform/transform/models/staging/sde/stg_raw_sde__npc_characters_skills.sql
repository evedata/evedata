with
    source as (select * from {{ source("raw_sde", "npc_characters__skills") }}),

    renamed as (

        select type_id as skill_id, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
