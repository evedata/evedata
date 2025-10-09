with
    source as (select * from {{ source("raw_sde", "masteries___value___value") }}),

    renamed as (

        select value as skill_type_id, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
