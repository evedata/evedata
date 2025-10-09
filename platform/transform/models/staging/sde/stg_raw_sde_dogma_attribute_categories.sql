with
    source as (select * from {{ source("raw_sde", "dogma_attribute_categories") }}),

    renamed as (

        select
            _key as dogma_attribute_category_id,
            description,
            name,
            _sde_version,
            _dlt_load_id,
            _dlt_id

        from source

    )

select *
from renamed
