import pytest
from pydantic import ValidationError

from dappydogs_chatbot_api.settings import Settings


def test_settings_accept_valid_values() -> None:
    settings = Settings(
        environment="development",
        service_name="chatbot-test",
    )

    assert settings.environment == "development"
    assert settings.service_name == "chatbot-test"
    assert settings.is_production is False


@pytest.mark.parametrize("service_name", ["", "   "])
def test_settings_reject_empty_service_name(service_name: str) -> None:
    with pytest.raises(ValidationError):
        Settings(service_name=service_name)


def test_settings_reject_unknown_environment() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="staging")  # type: ignore[arg-type]
