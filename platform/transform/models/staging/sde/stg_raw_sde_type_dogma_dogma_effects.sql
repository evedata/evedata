with
    source as (select * from {{ source("raw_sde", "type_dogma__dogma_effects") }}),

    renamed as (

        select effect_id, is_default, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
