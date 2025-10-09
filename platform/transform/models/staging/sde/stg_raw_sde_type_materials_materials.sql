with
    source as (select * from {{ source("raw_sde", "type_materials__materials") }}),

    renamed as (

        select material_type_id, quantity, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
