from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.ports.pets import (
    RegisteredPetsRepository,
    RegisteredPetsSourceError,
)


class RegisteredPetsUnavailableError(Exception):
    """Signal a controlled pet-directory dependency failure."""


class GetRegisteredPets:
    def __init__(self, repository: RegisteredPetsRepository) -> None:
        self._repository = repository

    def execute(self, principal: AuthenticatedPrincipal) -> Mapping[str, Any]:
        try:
            directory = self._repository.list_for(principal)
        except RegisteredPetsSourceError as error:
            raise RegisteredPetsUnavailableError from error
        return MappingProxyType(
            {
                "count": directory.total_count,
                "pets": tuple(
                    {"reference": pet.reference, "name": pet.name} for pet in directory.pets
                ),
            }
        )
