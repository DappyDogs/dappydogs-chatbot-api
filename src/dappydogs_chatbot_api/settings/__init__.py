from functools import lru_cache
from math import isfinite
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
    max_request_body_bytes: int = 1_048_576
    request_timeout_seconds: float = 30.0

    @field_validator("service_name")
    @classmethod
    def validate_service_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("service_name cannot be empty")
        return value

    @field_validator("max_request_body_bytes")
    @classmethod
    def validate_max_request_body_bytes(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("max_request_body_bytes must be positive")
        return value

    @field_validator("request_timeout_seconds")
    @classmethod
    def validate_request_timeout_seconds(cls, value: float) -> float:
        if not isfinite(value) or value <= 0:
            raise ValueError("request_timeout_seconds must be finite and positive")
        return value

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


__all__ = ["Settings", "get_settings"]
