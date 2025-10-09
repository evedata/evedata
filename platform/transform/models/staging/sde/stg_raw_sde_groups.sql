with
    source as (select * from {{ source("raw_sde", "groups") }}),

    renamed as (

        select
            _key as group_id,
            anchorable,
            anchored,
            category_id,
            fittable_non_singleton,
            name__de,
            name__en,
            name__es,
            name__fr,
            name__ja,
            name__ko,
            name__ru,
            name__zh,
            published,
            use_base_price,
            _sde_version,
            _dlt_load_id,
            _dlt_id,
            icon_id

        from source

    )

select *
from renamed
