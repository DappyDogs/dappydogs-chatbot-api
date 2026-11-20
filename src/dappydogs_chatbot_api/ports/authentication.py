from dataclasses import dataclass
from typing import Protocol


class TokenVerificationError(Exception):
    """A token could not be verified without exposing provider details."""


@dataclass(frozen=True, slots=True)
class VerifiedUserIdentity:
    uid: str


@dataclass(frozen=True, slots=True)
class VerifiedAppIdentity:
    app_id: str


class UserTokenVerifier(Protocol):
    def verify_user_token(self, token: str) -> VerifiedUserIdentity: ...


class AppTokenVerifier(Protocol):
    def verify_app_token(self, token: str) -> VerifiedAppIdentity: ...
