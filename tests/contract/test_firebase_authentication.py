from collections.abc import Mapping
from typing import Any

import pytest
from jwt import PyJWKClientError

from dappydogs_chatbot_api.adapters.firebase_authentication import FirebaseTokenVerifier
from dappydogs_chatbot_api.ports.authentication import TokenVerificationError


def test_firebase_user_verification_checks_revocation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    received: dict[str, Any] = {}

    def verify_id_token(
        token: str,
        app: object | None = None,
        check_revoked: bool = False,
    ) -> Mapping[str, Any]:
        received.update(token=token, app=app, check_revoked=check_revoked)
        return {"uid": "verified-user", "sub": "verified-user"}

    monkeypatch.setattr(
        "dappydogs_chatbot_api.adapters.firebase_authentication.auth.verify_id_token",
        verify_id_token,
    )

    identity = FirebaseTokenVerifier().verify_user_token("signed-user-token")

    assert identity.uid == "verified-user"
    assert received == {
        "token": "signed-user-token",
        "app": None,
        "check_revoked": True,
    }


def test_firebase_app_check_verification_maps_app_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "dappydogs_chatbot_api.adapters.firebase_authentication.app_check.verify_token",
        lambda token, app=None: {"app_id": "verified-app"},
    )

    identity = FirebaseTokenVerifier().verify_app_token("signed-app-token")

    assert identity.app_id == "verified-app"


@pytest.mark.parametrize(
    "claims",
    [
        {},
        {"uid": "user", "sub": "other-user"},
        {"uid": "", "sub": ""},
        {"uid": 123, "sub": "123"},
    ],
)
def test_firebase_user_verification_rejects_incompatible_claims(
    claims: Mapping[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "dappydogs_chatbot_api.adapters.firebase_authentication.auth.verify_id_token",
        lambda token, app=None, check_revoked=False: claims,
    )

    with pytest.raises(TokenVerificationError):
        FirebaseTokenVerifier().verify_user_token("signed-user-token")


@pytest.mark.parametrize("claims", [{}, {"app_id": ""}, {"app_id": 123}])
def test_firebase_app_verification_rejects_invalid_claims(
    claims: Mapping[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "dappydogs_chatbot_api.adapters.firebase_authentication.app_check.verify_token",
        lambda token, app=None: claims,
    )

    with pytest.raises(TokenVerificationError):
        FirebaseTokenVerifier().verify_app_token("signed-app-token")


def test_firebase_app_verification_sanitizes_signing_key_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_verification(token: str, app: object | None = None) -> Mapping[str, Any]:
        raise PyJWKClientError("sensitive signing-key endpoint detail")

    monkeypatch.setattr(
        "dappydogs_chatbot_api.adapters.firebase_authentication.app_check.verify_token",
        fail_verification,
    )

    with pytest.raises(TokenVerificationError) as captured:
        FirebaseTokenVerifier().verify_app_token("signed-app-token")

    assert str(captured.value) == ""
