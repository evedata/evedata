"""Provides utilities for working with JSON."""

from pathlib import Path
from typing import Any

import orjson as json


def load_json_file(path: str | Path) -> dict[str, Any] | list[Any]:
    """Load a JSON file."""
    full_path = Path(path).resolve()
    with full_path.open("r", encoding="utf-8") as file:
        return json.loads(file.read())
