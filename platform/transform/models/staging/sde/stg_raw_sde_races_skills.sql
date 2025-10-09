with
    source as (select * from {{ source("raw_sde", "races__skills") }}),

    renamed as (

        select
            _key as skill_type_id,
            _value as level,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id

        from source

    )

select *
from renamed
