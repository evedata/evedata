import tempfile
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

EVEDATA_ROOT = Path(__file__).parent.parent.parent.parent.parent
PROJECT_ROOT = Path(__file__).parent.parent.parent


def _env_prefix(env: str) -> str:
    if env == "production":
        return "prd"
    if env == "staging":
        return "stg"
    if env == "development":
        return "dev"
    if env == "test":
        return "tst"

    msg = f"Unknown environment: {env}"
    raise ValueError(msg)


def _r2_bucket_name(name: str, env: str, region: str) -> str:
    return "-".join([_env_prefix(env), name, region])


class Configuration(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="EVEDATA_PLATFORM_",
        env_nested_delimiter="__",
        env_parse_enums=True,
    )

    env: str = "production"

    root: Path = EVEDATA_ROOT
    home: Path = EVEDATA_ROOT
    cache_dir: Path = Field(default_factory=lambda: Path("/var/cache/evedata"))
    config_dir: Path = Field(default_factory=lambda: Path("/etc/evedata"))
    data_dir: Path = Field(default_factory=lambda: Path("/var/lib/evedata"))
    log_dir: Path = Field(default_factory=lambda: Path("/var/log/evedata"))
    run_dir: Path = Field(default_factory=lambda: Path("/run/evedata"))
    tmp_dir: Path = Field(
        default_factory=lambda: Path(tempfile.gettempdir()) / "evedata"
    )

    duckdb_path: Path = Field(
        default_factory=lambda data: data["data_dir"] / "evedata.duckdb"
    )
    http_cache_dir: Path = Field(
        default_factory=lambda data: data["cache_dir"] / "http"
    )
    state_dir: Path = Field(default_factory=lambda data: data["data_dir"] / "state")
    staging_dir: Path = Field(
        default_factory=lambda data: data["state_dir"] / "staging"
    )
    sde_staging_dir: Path = Field(
        default_factory=lambda data: data["staging_dir"] / "sde"
    )
    hde_staging_dir: Path = Field(
        default_factory=lambda data: data["staging_dir"] / "hde"
    )

    cloudflare_account_id: str = ""
    cloudflare_api_token: str = ""

    postgres_host: str
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: str
    postgres_database: str = "evedata"

    ducklake_host: str
    ducklake_port: int = 5433
    ducklake_user: str
    ducklake_password: str
    ducklake_database: str = "ducklake"

    r2_endpoint_url: str = Field(
        default_factory=lambda data: f"https://{data['cloudflare_account_id']}.r2.cloudflarestorage.com"
    )
    r2_region: str = "weur"
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_datasets_bucket: str = Field(
        default_factory=lambda data: _r2_bucket_name(
            "datasets", data["env"], data["r2_region"]
        )
    )
    r2_lake_bucket: str = Field(
        default_factory=lambda data: _r2_bucket_name(
            "lake", data["env"], data["r2_region"]
        )
    )
    r2_sources_bucket: str = Field(
        default_factory=lambda data: _r2_bucket_name(
            "sources", data["env"], data["r2_region"]
        )
    )


_config = Configuration()  # pyright: ignore[reportCallIssue]


def get_config() -> Configuration:
    return _config
