"""Provides utilities for working with YAML files."""

from pathlib import Path
from typing import Any

import yaml
from yaml import CSafeLoader as Loader


def load_yaml_file(file_path: str | Path) -> Any:
    """Load a YAML file."""
    full_path = Path(file_path).resolve()
    with full_path.open("r", encoding="utf-8") as file:
        return yaml.load(file, Loader=Loader)
