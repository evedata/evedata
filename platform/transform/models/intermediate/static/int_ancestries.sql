with
    ancestries as (
        select
            ancestry_id,
            bloodline_id,
            icon_id,
            description_en,
            name_en,
            charisma,
            intelligence,
            memory,
            perception,
            willpower
        from {{ ref("stg_sde_ancestries") }}
    )

select *
from ancestries
