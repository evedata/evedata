with
    source as (select * from {{ source("raw_hde", "graphicmaterialsets") }}),

    renamed as (

        select
            _key,
            color_primary__a,
            color_primary__b,
            color_primary__g,
            color_primary__n_sequence_fields,
            color_primary__n_unnamed_fields,
            color_primary__r,
            color_primary__n_fields,
            description,
            color_hull__a,
            color_hull__b,
            color_hull__g,
            color_hull__n_sequence_fields,
            color_hull__n_unnamed_fields,
            color_hull__r,
            color_hull__n_fields,
            sof_faction_name,
            color_window__a,
            color_window__b,
            color_window__g,
            color_window__n_sequence_fields,
            color_window__n_unnamed_fields,
            color_window__r,
            color_window__n_fields,
            color_secondary__a,
            color_secondary__b,
            color_secondary__g,
            color_secondary__n_sequence_fields,
            color_secondary__n_unnamed_fields,
            color_secondary__r,
            color_secondary__n_fields,
            sof_race_hint,
            _hde_version,
            _dlt_load_id,
            _dlt_id,
            material1,
            material4,
            material3,
            sof_pattern_name,
            custommaterial1,
            custommaterial2,
            material2,
            res_path_insert

        from source

    )

select *
from renamed
