with
    source as (
        select * from {{ source("hde_raw", "dynamic_item_attributes__attribute_ids") }}
    ),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as industry_mutaplasmid_attribute_uuid,
            _dlt_parent_id::text as industry_mutaplasmid_uuid,
            id::bigint as attribute_id,

            -- -------- Numerics
            max::decimal as maximum,
            min::decimal as minimum,

            -- -------- Booleans
            case
                when high_is_good::smallint = 0
                then false
                when high_is_good::smallint = 1
                then true
            end as high_is_good

        from source
    )

select *
from renamed
