from typing import Annotated

import pytest
from fastapi import Body, FastAPI
from httpx import ASGITransport, AsyncClient, Response
from pydantic import BaseModel, ConfigDict

from dappydogs_chatbot_api.api.app import create_app
from dappydogs_chatbot_api.api.authentication import MAX_TOKEN_LENGTH, Principal
from dappydogs_chatbot_api.application.authentication import AuthenticateRequest
from dappydogs_chatbot_api.ports.authentication import (
    TokenVerificationError,
    VerifiedAppIdentity,
    VerifiedUserIdentity,
)
from dappydogs_chatbot_api.settings import Settings

pytestmark = pytest.mark.anyio


class ControlledUserVerifier:
    def verify_user_token(self, token: str) -> VerifiedUserIdentity:
        if token != "valid-user-token":
            raise TokenVerificationError("sensitive SDK detail")
        return VerifiedUserIdentity(uid="server-verified-user")


class ControlledAppVerifier:
    def verify_app_token(self, token: str) -> VerifiedAppIdentity:
        if token != "valid-app-token":
            raise TokenVerificationError("sensitive App Check claim")
        return VerifiedAppIdentity(app_id="server-verified-app")


class ForgedIdentityPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    uid: str


def build_protected_app() -> tuple[FastAPI, list[str]]:
    authenticator = AuthenticateRequest(ControlledUserVerifier(), ControlledAppVerifier())
    app = create_app(Settings(), authenticator=authenticator)
    executed_for: list[str] = []

    @app.post("/protected")
    async def protected_endpoint(
        principal: Principal,
        payload: Annotated[ForgedIdentityPayload, Body()],
    ) -> dict[str, str]:
        executed_for.append(principal.uid)
        return {
            "uid": principal.uid,
            "app_id": principal.app_id,
            "payload_uid": payload.uid,
        }

    return app, executed_for


async def request_protected(
    *,
    headers: dict[str, str] | list[tuple[str, str]] | None = None,
    uid: str = "forged-user",
) -> tuple[Response, list[str]]:
    app, executed_for = build_protected_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/protected", headers=headers, json={"uid": uid})
    return response, executed_for


async def test_verified_principal_cannot_be_replaced_by_payload_uid() -> None:
    response, executed_for = await request_protected(
        headers={
            "Authorization": "Bearer valid-user-token",
            "X-Firebase-AppCheck": "valid-app-token",
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "uid": "server-verified-user",
        "app_id": "server-verified-app",
        "payload_uid": "forged-user",
    }
    assert executed_for == ["server-verified-user"]


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": "Bearer valid-user-token"},
        {"X-Firebase-AppCheck": "valid-app-token"},
        {
            "Authorization": "Basic valid-user-token",
            "X-Firebase-AppCheck": "valid-app-token",
        },
        {
            "Authorization": "Bearer invalid-user-token",
            "X-Firebase-AppCheck": "valid-app-token",
        },
        {
            "Authorization": "Bearer valid-user-token",
            "X-Firebase-AppCheck": "invalid-app-token",
        },
        {
            "Authorization": f"Bearer {'x' * (MAX_TOKEN_LENGTH + 1)}",
            "X-Firebase-AppCheck": "valid-app-token",
        },
    ],
)
async def test_invalid_evidence_is_rejected_before_endpoint_execution(
    headers: dict[str, str],
) -> None:
    response, executed_for = await request_protected(headers=headers)

    assert response.status_code == 401
    assert executed_for == []
    serialized = response.text
    assert "invalid-user-token" not in serialized
    assert "invalid-app-token" not in serialized
    assert "SDK" not in serialized
    assert "claim" not in serialized


async def test_duplicate_authentication_headers_are_rejected() -> None:
    response, executed_for = await request_protected(
        headers=[
            ("Authorization", "Bearer valid-user-token"),
            ("Authorization", "Bearer second-user-token"),
            ("X-Firebase-AppCheck", "valid-app-token"),
        ]
    )

    assert response.status_code == 401
    assert executed_for == []
