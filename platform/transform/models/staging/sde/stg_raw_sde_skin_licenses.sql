with
    source as (select * from {{ source("raw_sde", "skin_licenses") }}),

    renamed as (

        select
            _key as skin_license_id,
            duration,
            license_type_id,
            skin_id,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            is_single_use

        from source

    )

select *
from renamed
