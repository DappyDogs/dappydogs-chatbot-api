from functools import lru_cache
from math import isfinite
from typing import Literal
from urllib.parse import urlparse

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
    model_provider: str = "ollama"
    model_base_url: str = "http://127.0.0.1:11434"
    model_name: str = "llama3.1:8b"
    model_timeout_seconds: float = 120.0

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

    @field_validator("model_provider", "model_name")
    @classmethod
    def validate_model_identifier(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("model identifiers cannot be empty")
        return normalized

    @field_validator("model_base_url")
    @classmethod
    def validate_model_base_url(cls, value: str) -> str:
        normalized = value.rstrip("/")
        parsed = urlparse(normalized)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("model_base_url must be an absolute HTTP URL")
        if parsed.path or parsed.params or parsed.query or parsed.fragment:
            raise ValueError("model_base_url cannot contain a path, query, or fragment")
        return normalized

    @field_validator("model_timeout_seconds")
    @classmethod
    def validate_model_timeout_seconds(cls, value: float) -> float:
        if not isfinite(value) or value <= 0:
            raise ValueError("model_timeout_seconds must be finite and positive")
        return value

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()


__all__ = ["Settings", "get_settings"]
