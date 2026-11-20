from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from dappydogs_chatbot_api.api.app import create_app
from dappydogs_chatbot_api.settings import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings(environment="local")


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client(settings: Settings) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=create_app(settings))
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client
