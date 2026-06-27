from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_path: Path = Field(default=Path.home() / ".logy" / "data" / "logy.db")
    graph_dir: Path = Field(default=Path.home() / ".logy" / "data" / "graph")
    litellm_model: str = Field(default="gpt-4o-mini")
    litellm_api_key: str | None = Field(default=None)
    litellm_api_base: str | None = Field(default=None)
    server_host: str = Field(default="127.0.0.1")
    server_port: int = Field(default=8080)

    model_config = {"env_prefix": "LOGY_"}


settings = Settings()
