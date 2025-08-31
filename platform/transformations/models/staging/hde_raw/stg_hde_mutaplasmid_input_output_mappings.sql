with
    source as (
        select *
        from {{ source("hde_raw", "dynamic_item_attributes__input_output_mapping") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as mutaplasmid_input_output_mapping_uuid,
            _dlt_parent_id::text as mutaplasmid_uuid,
            resulting_type::bigint as output_type_id

        from source
    )

select *
from renamed
