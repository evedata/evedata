with
    source as (select * from {{ source("hde_raw", "dynamic_item_attributes") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as mutaplasmid_uuid,
            id::bigint as type_id,

            -- -------- Text
            hde_version::text as hde_version

        from source
    )

select *
from renamed
