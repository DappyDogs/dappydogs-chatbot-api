from typing import Protocol

from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.pets import RegisteredPetsDirectory


class RegisteredPetsRepository(Protocol):
    def list_for(self, principal: AuthenticatedPrincipal) -> RegisteredPetsDirectory: ...


class RegisteredPetsSourceError(Exception):
    """Signal an unavailable pet directory without exposing source details."""
