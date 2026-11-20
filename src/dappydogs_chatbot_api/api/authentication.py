from typing import Annotated

from fastapi import Depends, Request

from dappydogs_chatbot_api.application.authentication import (
    AuthenticateRequest,
    AuthenticationEvidence,
)
from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.errors import (
    AuthenticationConfigurationError,
    AuthenticationRequiredError,
    InvalidAuthenticationError,
)

AUTHORIZATION_HEADER = "authorization"
APP_CHECK_HEADER = "x-firebase-appcheck"
MAX_TOKEN_LENGTH = 8192


def extract_authentication_evidence(request: Request) -> AuthenticationEvidence:
    authorization = _single_header(request, AUTHORIZATION_HEADER)
    app_token = _single_header(request, APP_CHECK_HEADER)

    scheme, separator, user_token = authorization.partition(" ")
    if separator != " " or scheme.casefold() != "bearer" or not user_token:
        raise InvalidAuthenticationError
    if any(character.isspace() for character in user_token):
        raise InvalidAuthenticationError
    _validate_token(app_token)
    _validate_token(user_token)
    return AuthenticationEvidence(user_token=user_token, app_token=app_token)


def _single_header(request: Request, name: str) -> str:
    values = request.headers.getlist(name)
    if not values:
        raise AuthenticationRequiredError
    if len(values) != 1:
        raise InvalidAuthenticationError
    return values[0]


def _validate_token(token: str) -> None:
    if not token or len(token) > MAX_TOKEN_LENGTH:
        raise InvalidAuthenticationError
    if any(character.isspace() for character in token):
        raise InvalidAuthenticationError


def require_authenticated_principal(request: Request) -> AuthenticatedPrincipal:
    authenticator = getattr(request.app.state, "authenticator", None)
    if not isinstance(authenticator, AuthenticateRequest):
        raise AuthenticationConfigurationError
    evidence = extract_authentication_evidence(request)
    return authenticator.execute(evidence)


Principal = Annotated[AuthenticatedPrincipal, Depends(require_authenticated_principal)]
