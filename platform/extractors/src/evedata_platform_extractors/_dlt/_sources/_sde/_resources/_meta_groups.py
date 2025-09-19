from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from evedata_platform_extractors._types import ResourceConfig


def _before_load_meta_group(record: dict[str, Any]) -> dict[str, Any]:
    if "color" in record:
        color = record.pop("color")
        new_color = {"r": color[0], "g": color[1], "b": color[2], "a": color[3]}
        record["color"] = new_color

    return record


meta_groups_config: "ResourceConfig" = {
    "before_load": [_before_load_meta_group],
}
