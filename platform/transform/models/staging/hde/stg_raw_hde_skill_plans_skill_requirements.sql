with
    source as (select * from {{ source("raw_hde", "skillplans__skill_requirements") }}),

    renamed as (

        select type_id, level, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
