from collections.abc import Mapping
from typing import Any

from firebase_admin import App, app_check, auth  # type: ignore[import-untyped]
from firebase_admin.exceptions import FirebaseError  # type: ignore[import-untyped]
from jwt import PyJWKClientError

from dappydogs_chatbot_api.ports.authentication import (
    TokenVerificationError,
    VerifiedAppIdentity,
    VerifiedUserIdentity,
)


class FirebaseTokenVerifier:
    """Verify Firebase Auth and App Check tokens through the Admin SDK."""

    def __init__(self, firebase_app: App | None = None) -> None:
        self._firebase_app = firebase_app

    def verify_user_token(self, token: str) -> VerifiedUserIdentity:
        try:
            claims = auth.verify_id_token(
                token,
                app=self._firebase_app,
                check_revoked=True,
            )
            uid = self._required_string_claim(claims, "uid")
            subject = self._required_string_claim(claims, "sub")
            if uid != subject:
                raise ValueError("uid and subject claims differ")
            return VerifiedUserIdentity(uid=uid)
        except (FirebaseError, KeyError, TypeError, ValueError) as error:
            raise TokenVerificationError from error

    def verify_app_token(self, token: str) -> VerifiedAppIdentity:
        try:
            claims = app_check.verify_token(token, app=self._firebase_app)
            return VerifiedAppIdentity(app_id=self._required_string_claim(claims, "app_id"))
        except (FirebaseError, PyJWKClientError, KeyError, TypeError, ValueError) as error:
            raise TokenVerificationError from error

    @staticmethod
    def _required_string_claim(claims: Mapping[str, Any], name: str) -> str:
        value = claims[name]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"claim {name!r} must be a non-empty string")
        return value
