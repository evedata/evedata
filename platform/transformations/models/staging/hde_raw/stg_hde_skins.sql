with
    source as (select * from {{ source("hde_raw", "skins") }}),

    renamed as (
        select
            -- -------- IDs
            _dlt_id::text as skin_uuid,
            id::bigint as skin_id,
            skin_material_id::bigint as skin_material_id,

            -- -------- Text
            internal_name::text as internal_name,
            skin_description::text as skin_description,

            -- -------- Booleans
            allow_ccp_devs::boolean as allows_ccp_devs,
            is_structure_skin::boolean as is_structure_skin,
            visible_serenity::boolean as is_visible_serenity,
            visible_tranquility::boolean as is_visible_tranquility

        from source
    )

select *
from renamed
