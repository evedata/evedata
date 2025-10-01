with
    source as (select * from {{ source("hde_raw", "graphic_material_sets") }}),

    renamed as (
        select

            -- -------- IDs
            _dlt_id::text as graphic_material_set_uuid,
            id::bigint as graphic_material_set_id,

            -- -------- Text
            custommaterial1::text as custom_material_1,
            custommaterial2::text as custom_material_2,
            description::text as description,
            hde_version::text as hde_version,
            material1::text as material_1,
            material2::text as material_2,
            material3::text as material_3,
            material4::text as material_4,
            res_path_insert::text as res_path_insert,
            sof_faction_name::text as sof_faction_name,
            sof_pattern_name::text as sof_pattern_name,
            sof_race_hint::text as sof_race_hint,

            -- -------- Numerics
            color_hull__a::decimal as color_hull_a,
            color_hull__b::decimal as color_hull_b,
            color_hull__g::decimal as color_hull_g,
            color_hull__n_fields::bigint as color_hull_n_fields,
            color_hull__n_sequence_fields::bigint as color_hull_n_sequence_fields,
            color_hull__n_unnamed_fields::bigint as color_hull_n_unnamed_fields,
            color_hull__r::decimal as color_hull_r,
            color_primary__a::decimal as color_primary_a,
            color_primary__b::decimal as color_primary_b,
            color_primary__g::decimal as color_primary_g,
            color_primary__n_fields::bigint as color_primary_n_fields,
            color_primary__n_sequence_fields::bigint as color_primary_n_sequence_fields,
            color_primary__n_unnamed_fields::bigint as color_primary_n_unnamed_fields,
            color_primary__r::decimal as color_primary_r,
            color_secondary__a::decimal as color_secondary_a,
            color_secondary__b::decimal as color_secondary_b,
            color_secondary__g::decimal as color_secondary_g,
            color_secondary__n_fields::bigint as color_secondary_n_fields,
            color_secondary__n_sequence_fields::bigint
            as color_secondary_n_sequence_fields,
            color_secondary__n_unnamed_fields::bigint
            as color_secondary_n_unnamed_fields,
            color_secondary__r::decimal as color_secondary_r,
            color_window__a::decimal as color_window_a,
            color_window__b::decimal as color_window_b,
            color_window__g::decimal as color_window_g,
            color_window__n_fields::bigint as color_window_n_fields,
            color_window__n_sequence_fields::bigint as color_window_n_sequence_fields,
            color_window__n_unnamed_fields::bigint as color_window_n_unnamed_fields,
            color_window__r::decimal as color_window_r

        from source
    )

select *
from renamed
