from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from evedata_static._types import ResourceConfig


npc_corporations_config: "ResourceConfig" = {
    "hints": {
        "columns": [
            {"name": "corporationTrades", "data_type": "json"},
            {"name": "exchangeRates", "data_type": "json"},
            {"name": "investors", "data_type": "json"},
            {"name": "lpOfferTables", "data_type": "json"},
        ],
    },
}
