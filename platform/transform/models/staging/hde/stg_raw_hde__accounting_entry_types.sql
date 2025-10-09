with
    source as (select * from {{ source("raw_hde", "accountingentrytypes") }}),

    renamed as (

        select
            _key,
            entry_type_name_id,
            entry_type_name_translated,
            description,
            name,
            _hde_version,
            _dlt_load_id,
            _dlt_id,
            entry_journal_message_translated,
            entry_journal_message_id,
            entry_type_description_translated,
            entry_type_description_id

        from source

    )

select *
from renamed
