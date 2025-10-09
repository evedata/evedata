with
    source as (

        select *
        from {{ source("raw_hde", "industryinstallationtypes__assembly_lines") }}

    ),

    renamed as (

        select assembly_line, _dlt_parent_id, _dlt_list_idx, _dlt_id from source

    )

select *
from renamed
