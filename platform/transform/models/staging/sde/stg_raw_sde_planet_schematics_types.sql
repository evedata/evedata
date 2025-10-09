with
    source as (select * from {{ source("raw_sde", "planet_schematics__types") }}),

    renamed as (

        select
            _key as type_id, is_input, quantity, _dlt_parent_id, _dlt_list_idx, _dlt_id

        from source

    )

select *
from renamed
