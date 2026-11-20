import pytest

from dappydogs_chatbot_api.application.authentication import (
    AuthenticateRequest,
    AuthenticationEvidence,
)
from dappydogs_chatbot_api.domain.errors import InvalidAuthenticationError
from dappydogs_chatbot_api.ports.authentication import (
    TokenVerificationError,
    VerifiedAppIdentity,
    VerifiedUserIdentity,
)


class UserVerifierStub:
    def __init__(self, uid: str = "verified-user", fails: bool = False) -> None:
        self.uid = uid
        self.fails = fails
        self.calls = 0

    def verify_user_token(self, token: str) -> VerifiedUserIdentity:
        self.calls += 1
        if self.fails:
            raise TokenVerificationError("provider diagnostic containing token")
        return VerifiedUserIdentity(uid=self.uid)


class AppVerifierStub:
    def __init__(self, app_id: str = "verified-app", fails: bool = False) -> None:
        self.app_id = app_id
        self.fails = fails

    def verify_app_token(self, token: str) -> VerifiedAppIdentity:
        if self.fails:
            raise TokenVerificationError("provider diagnostic containing claims")
        return VerifiedAppIdentity(app_id=self.app_id)


def test_authentication_evidence_repr_does_not_expose_tokens() -> None:
    evidence = AuthenticationEvidence("sensitive-user-token", "sensitive-app-token")

    assert "sensitive-user-token" not in repr(evidence)
    assert "sensitive-app-token" not in repr(evidence)


def test_authenticate_request_builds_an_immutable_server_principal() -> None:
    use_case = AuthenticateRequest(UserVerifierStub(), AppVerifierStub())

    principal = use_case.execute(AuthenticationEvidence("user-token", "app-token"))

    assert principal.uid == "verified-user"
    assert principal.app_id == "verified-app"
    with pytest.raises(AttributeError):
        principal.uid = "forged-user"  # type: ignore[misc]


@pytest.mark.parametrize("failing_side", ["user", "app"])
def test_authenticate_request_sanitizes_verifier_failures(failing_side: str) -> None:
    user_verifier = UserVerifierStub(fails=failing_side == "user")
    use_case = AuthenticateRequest(
        user_verifier,
        AppVerifierStub(fails=failing_side == "app"),
    )

    with pytest.raises(InvalidAuthenticationError) as captured:
        use_case.execute(AuthenticationEvidence("sensitive-user-token", "sensitive-app-token"))

    assert str(captured.value) == ""
    assert captured.value.public_message == "Authentication evidence is invalid."
    assert user_verifier.calls == (0 if failing_side == "app" else 1)


@pytest.mark.parametrize(("uid", "app_id"), [("", "app"), ("user", "")])
def test_authenticate_request_rejects_empty_verified_identifiers(uid: str, app_id: str) -> None:
    use_case = AuthenticateRequest(UserVerifierStub(uid=uid), AppVerifierStub(app_id=app_id))

    with pytest.raises(InvalidAuthenticationError):
        use_case.execute(AuthenticationEvidence("user-token", "app-token"))
