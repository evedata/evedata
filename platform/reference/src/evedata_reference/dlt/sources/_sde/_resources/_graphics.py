from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from evedata_reference.dlt.sources._types import ResourceConfig

graphics_config: "ResourceConfig" = {
    "hints": {
        "primary_key": "id",
        "columns": [{"name": "sofLayout", "data_type": "json"}],
    }
}
