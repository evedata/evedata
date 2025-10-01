with
    source as (
        select *
        from
            {{
                source(
                    "hde_raw",
                    "dynamic_item_attributes__input_output_mapping__applicable_types",
                )
            }}  -- noqa: LT05
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as mutaplasmid_input_output_mapping_type_uuid,
            _dlt_parent_id::text as mutaplasmid_uuid,
            value::bigint as input_type_id

        from source
    )

select *
from renamed
