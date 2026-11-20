from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DAPPYDOGS_",
        extra="forbid",
        frozen=True,
    )

    environment: Literal["local", "development", "production"] = "local"
    service_name: str = "dappydogs-chatbot-api"

    @field_validator("service_name")
    @classmethod
    def validate_service_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("service_name cannot be empty")
        return value

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


__all__ = ["Settings", "get_settings"]
