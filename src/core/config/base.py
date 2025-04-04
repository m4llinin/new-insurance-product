from typing import Any

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="env/dev.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_ignore_empty=True,
        extra="ignore",
    )

    @staticmethod
    def parse_to_list(v: Any) -> list[str]:
        return list(map(str, v.split(",")))
