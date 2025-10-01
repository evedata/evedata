with
    source as (select * from {{ source("hde_raw", "accounting_entry_types") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as accounting_entry_type_uuid,
            id::bigint as accounting_entry_type_id,
            entry_journal_message_id::bigint as entry_journal_message_id,
            entry_type_description_id::bigint as entry_type_description_id,
            entry_type_name_id::bigint as entry_type_name_id,

            -- -------- Text
            description::text as description,
            entry_journal_message_translated::text as entry_journal_message_translated,
            entry_type_description_translated::text
            as entry_type_description_translated,
            entry_type_name_translated::text as entry_type_name_translated,
            hde_version::text as hde_version,
            name::text as name

        from source
    )

select *
from renamed
