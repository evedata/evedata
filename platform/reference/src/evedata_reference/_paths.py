from pathlib import Path


def default_hde_path() -> Path:
    return Path.cwd() / "data" / "hde"


def default_sde_path() -> Path:
    return Path.cwd() / "data" / "sde"


def default_duckdb_path() -> Path:
    return Path.cwd() / "data" / "evedata_reference.duckdb"
