with
    source as (
        select unit_id, description, display_name, name
        from {{ ref("stg_hde_units") }}
        where valid_to is null
    )

select *
from source
