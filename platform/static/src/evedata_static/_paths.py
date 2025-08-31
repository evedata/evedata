from os import getenv
from pathlib import Path


def _env_or_path(env_var: str, default_path: Path) -> Path:
    return Path(getenv(env_var, default_path))


def default_hde_path() -> Path:
    return _env_or_path("EVEDATA_STATIC_HDE_PATH", Path.cwd() / "data" / "hde")


def default_sde_path() -> Path:
    return _env_or_path("EVEDATA_STATIC_SDE_PATH", Path.cwd() / "data" / "sde")


def default_duckdb_path() -> Path:
    return _env_or_path(
        "EVEDATA_DATABASE_PATH", Path.cwd() / "data" / "evedata_static.duckdb"
    )
