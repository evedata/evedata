with
    source as (select * from {{ source("raw_sde", "type_bonus__misc_bonuses") }}),

    renamed as (

        select
            bonus_text__de,
            bonus_text__en,
            bonus_text__es,
            bonus_text__fr,
            bonus_text__ja,
            bonus_text__ko,
            bonus_text__ru,
            bonus_text__zh,
            importance,
            is_positive,
            _dlt_parent_id,
            _dlt_list_idx,
            _dlt_id,
            bonus,
            unit_id

        from source

    )

select *
from renamed
