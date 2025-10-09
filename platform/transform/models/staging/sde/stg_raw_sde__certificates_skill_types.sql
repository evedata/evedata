with
    source as (select * from {{ source("raw_sde", "certificates__skill_types") }}),

    renamed as (

        select
            _key as skill_type_id,
            advanced,
            basic,
            elite,
            improved,
            standard,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id

        from source

    )

select *
from renamed
