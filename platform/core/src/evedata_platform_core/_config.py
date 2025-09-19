from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

EVEDATA_ROOT = Path(__file__).parent.parent.parent.parent.parent
PROJECT_ROOT = Path(__file__).parent.parent.parent


class Configuration(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="EVEDATA_",
        env_nested_delimiter="__",
        env_parse_enums=True,
    )

    env: str = "development"

    root: Path = EVEDATA_ROOT
    home: Path = EVEDATA_ROOT
    cache_path: Path = Field(default_factory=lambda data: data["home"] / "cache")
    config_path: Path = Field(default_factory=lambda data: data["home"] / "config")
    data_path: Path = Field(default_factory=lambda data: data["home"] / "data")
    log_path: Path = Field(default_factory=lambda data: data["home"] / "logs")
    tmp_path: Path = Field(default_factory=lambda data: data["home"] / "tmp")

    duckdb_path: Path = Field(
        default_factory=lambda data: data["data_path"] / "evedata.duckdb"
    )
    hde_path: Path = Field(default_factory=lambda data: data["data_path"] / "hde")
    sde_path: Path = Field(default_factory=lambda data: data["data_path"] / "sde")

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"  # noqa: S105
    postgres_db: str = "evedata"


_config = Configuration()


def get_config() -> Configuration:
    return _config
