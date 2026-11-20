import pytest
from httpx import ASGITransport, AsyncClient

from dappydogs_chatbot_api.api.app import create_app
from dappydogs_chatbot_api.domain.errors import ApplicationError
from dappydogs_chatbot_api.settings import Settings

pytestmark = pytest.mark.anyio


async def test_liveness_does_not_require_external_services(client: AsyncClient) -> None:
    response = await client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive", "service": "dappydogs-chatbot-api"}


async def test_readiness_has_an_explicit_contract(client: AsyncClient) -> None:
    response = await client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "service": "dappydogs-chatbot-api"}


async def test_unknown_route_uses_framework_not_found_contract(client: AsyncClient) -> None:
    response = await client.get("/does-not-exist")

    assert response.status_code == 404


async def test_application_error_is_exposed_as_a_sanitized_response() -> None:
    app = create_app(Settings())

    @app.get("/failure")
    async def failure() -> None:
        raise ApplicationError("internal diagnostic")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/failure")

    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "application_error",
            "message": "The operation could not be completed.",
        }
    }
    assert "internal diagnostic" not in response.text
