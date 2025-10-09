with
    source as (select * from {{ source("raw_hde", "_dlt_version") }}),

    renamed as (

        select version, engine_version, inserted_at, schema_name, version_hash, schema

        from source

    )

select *
from renamed
