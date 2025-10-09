with
    source as (select * from {{ source("raw_sde", "dogma_effects__modifier_info") }}),

    renamed as (

        select
            domain,
            func,
            modified_attribute_id,
            modifying_attribute_id,
            operation,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id,
            group_id,
            skill_type_id,
            effect_id

        from source

    )

select *
from renamed
