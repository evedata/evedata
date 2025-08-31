with
    source as (select * from {{ source("sde_raw", "dogma_effects__modifier_info") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as effect_modifier_uuid,
            _dlt_parent_id::text as effect_uuid,
            _dlt_list_idx::smallint as effect_modifier_index,
            group_id::bigint as group_id,
            modified_attribute_id::bigint as modified_attribute_id,
            modifying_attribute_id::bigint as modifying_attribute_id,
            skill_type_id::bigint as skill_type_id,

            -- -------- Text
            domain::text as domain,
            func::text as func,
            operation::bigint as operator

        from source
    )

select *
from renamed
