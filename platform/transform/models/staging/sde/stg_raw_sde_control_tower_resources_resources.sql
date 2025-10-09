with
    source as (

        select * from {{ source("raw_sde", "control_tower_resources__resources") }}

    ),

    renamed as (

        select
            purpose,
            quantity,
            resource_type_id,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id,
            faction_id,
            min_security_level

        from source

    )

select *
from renamed
