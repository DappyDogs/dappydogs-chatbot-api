import asyncio
import json
import logging
from collections.abc import AsyncIterator

import pytest
from fastapi import Body
from httpx import ASGITransport, AsyncClient

from dappydogs_chatbot_api.api.app import create_app
from dappydogs_chatbot_api.api.http import API_V1_PREFIX, JsonLogFormatter
from dappydogs_chatbot_api.settings import Settings

pytestmark = pytest.mark.anyio


async def test_every_response_has_a_server_generated_request_id(client: AsyncClient) -> None:
    supplied_id = "user@example.com"

    response = await client.get("/health/live", headers={"X-Request-ID": supplied_id})

    request_id = response.headers["x-request-id"]
    assert request_id != supplied_id
    assert len(request_id) == 32
    int(request_id, 16)


async def test_framework_errors_use_the_stable_envelope(client: AsyncClient) -> None:
    response = await client.get("/missing?prompt=private")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "not_found",
            "message": "The requested resource was not found.",
            "request_id": response.headers["x-request-id"],
        }
    }
    assert "private" not in response.text


async def test_method_rejection_preserves_only_the_allow_header(client: AsyncClient) -> None:
    response = await client.post("/health/live")

    assert response.status_code == 405
    assert response.headers["allow"] == "GET"
    assert response.json()["error"]["code"] == "http_error"


async def test_validation_errors_do_not_expose_inputs() -> None:
    app = create_app(Settings())

    @app.post(f"{API_V1_PREFIX}/validate")
    async def validate(value: int = Body()) -> None:
        return None

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(f"{API_V1_PREFIX}/validate", json="private prompt")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"
    assert "private prompt" not in response.text


async def test_declared_oversized_body_is_rejected_before_endpoint_execution() -> None:
    executed = False
    app = create_app(Settings(max_request_body_bytes=8))

    @app.post(f"{API_V1_PREFIX}/body")
    async def consume_body(payload: bytes = Body()) -> None:
        nonlocal executed
        executed = True

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(f"{API_V1_PREFIX}/body", content=b"0123456789")

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "request_too_large"
    assert executed is False


async def test_streamed_oversized_body_is_rejected_without_content_length() -> None:
    executed = False
    app = create_app(Settings(max_request_body_bytes=8))

    @app.post(f"{API_V1_PREFIX}/stream")
    async def consume_stream(payload: bytes = Body()) -> None:
        nonlocal executed
        executed = True

    async def chunks() -> AsyncIterator[bytes]:
        yield b"12345"
        yield b"67890"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(f"{API_V1_PREFIX}/stream", content=chunks())

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "request_too_large"
    assert executed is False


@pytest.mark.parametrize("content_length", ["invalid", "-1", "1, 1"])
async def test_invalid_content_length_is_rejected(content_length: str) -> None:
    app = create_app(Settings())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            f"{API_V1_PREFIX}/missing",
            headers={"Content-Length": content_length},
            content=b"x",
        )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_request"


async def test_timeout_cancels_the_endpoint() -> None:
    cancelled = asyncio.Event()
    app = create_app(Settings(request_timeout_seconds=0.01))

    @app.get(f"{API_V1_PREFIX}/slow")
    async def slow() -> None:
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            cancelled.set()
            raise

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"{API_V1_PREFIX}/slow")

    assert response.status_code == 504
    assert response.json()["error"]["code"] == "request_timeout"
    assert cancelled.is_set()


async def test_unexpected_failures_are_sanitized_in_responses_and_logs(
    caplog: pytest.LogCaptureFixture,
) -> None:
    app = create_app(Settings())

    @app.get(f"{API_V1_PREFIX}/failure")
    async def failure() -> None:
        raise RuntimeError("secret-token private-prompt")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"{API_V1_PREFIX}/failure")

    serialized = response.text + caplog.text
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "internal_error"
    assert "secret-token" not in serialized
    assert "private-prompt" not in serialized
    assert "Traceback" not in serialized


def test_http_log_formatter_produces_structured_allowlisted_json() -> None:
    record = logging.LogRecord(
        name="dappydogs_chatbot_api.http",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request_completed",
        args=(),
        exc_info=None,
    )
    record.request_id = "safe-id"
    record.method = "POST"
    record.route = "/api/v1/example"
    record.status_code = 200
    record.untrusted_value = "secret-token private-prompt"

    payload = json.loads(JsonLogFormatter().format(record))

    assert payload == {
        "event": "request_completed",
        "level": "info",
        "logger": "dappydogs_chatbot_api.http",
        "method": "POST",
        "request_id": "safe-id",
        "route": "/api/v1/example",
        "status_code": 200,
    }
