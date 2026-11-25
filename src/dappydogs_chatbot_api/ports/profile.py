from typing import Protocol

from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.profile import ProfileLookup


class DogProfileRepository(Protocol):
    def get_for(
        self,
        principal: AuthenticatedPrincipal,
        *,
        pet_name: str | None = None,
    ) -> ProfileLookup: ...


class ProfileSourceError(Exception):
    """Signal an unavailable or malformed profile source without exposing its contents."""
