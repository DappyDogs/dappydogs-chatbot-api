from dataclasses import dataclass, field

from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.errors import InvalidAuthenticationError
from dappydogs_chatbot_api.ports.authentication import (
    AppTokenVerifier,
    TokenVerificationError,
    UserTokenVerifier,
)


@dataclass(frozen=True, slots=True)
class AuthenticationEvidence:
    user_token: str = field(repr=False)
    app_token: str = field(repr=False)


class AuthenticateRequest:
    def __init__(
        self,
        user_token_verifier: UserTokenVerifier,
        app_token_verifier: AppTokenVerifier,
    ) -> None:
        self._user_token_verifier = user_token_verifier
        self._app_token_verifier = app_token_verifier

    def execute(self, evidence: AuthenticationEvidence) -> AuthenticatedPrincipal:
        try:
            app_identity = self._app_token_verifier.verify_app_token(evidence.app_token)
            user_identity = self._user_token_verifier.verify_user_token(evidence.user_token)
            return AuthenticatedPrincipal(
                uid=user_identity.uid,
                app_id=app_identity.app_id,
            )
        except (TokenVerificationError, ValueError) as error:
            raise InvalidAuthenticationError from error
