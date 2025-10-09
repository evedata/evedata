with
    source as (select * from {{ source("raw_sde", "dbuff_collections") }}),

    renamed as (

        select
            _key as dbuff_collection_id,
            aggregate_mode,
            developer_description,
            operation_name,
            show_output_value_in_ui,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            display_name__de,
            display_name__en,
            display_name__es,
            display_name__fr,
            display_name__ja,
            display_name__ko,
            display_name__ru,
            display_name__zh

        from source

    )

select *
from renamed
