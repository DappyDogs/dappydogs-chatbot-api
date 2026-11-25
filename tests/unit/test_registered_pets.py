import pytest

from dappydogs_chatbot_api.application.pets import GetRegisteredPets
from dappydogs_chatbot_api.application.pets_tool import (
    RegisteredPetsToolArguments,
    RegisteredPetsToolHandler,
)
from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.pets import RegisteredPet, RegisteredPetsDirectory


class PetsRepository:
    def __init__(self, directory: RegisteredPetsDirectory) -> None:
        self._directory = directory

    def list_for(self, principal: AuthenticatedPrincipal) -> RegisteredPetsDirectory:
        del principal
        return self._directory


def principal() -> AuthenticatedPrincipal:
    return AuthenticatedPrincipal(uid="verified-user", app_id="verified-app")


def test_registered_pets_capability_supports_multiple_pets() -> None:
    capability = GetRegisteredPets(
        PetsRepository(
            RegisteredPetsDirectory(
                total_count=3,
                pets=(
                    RegisteredPet("pet-1", "Dappy"),
                    RegisteredPet("pet-2", "Nala"),
                    RegisteredPet("pet-3", None),
                ),
            )
        )
    )

    result = capability.execute(principal())

    assert result == {
        "count": 3,
        "pets": (
            {"reference": "pet-1", "name": "Dappy"},
            {"reference": "pet-2", "name": "Nala"},
            {"reference": "pet-3", "name": None},
        ),
    }


def test_registered_pets_tool_renders_count_and_available_names() -> None:
    handler = RegisteredPetsToolHandler(
        GetRegisteredPets(
            PetsRepository(
                RegisteredPetsDirectory(
                    total_count=3,
                    pets=(
                        RegisteredPet("pet-1", "Dappy"),
                        RegisteredPet("pet-2", "Nala"),
                        RegisteredPet("pet-3", None),
                    ),
                )
            )
        )
    )

    result = handler(principal(), RegisteredPetsToolArguments())

    assert result.final_response == (
        "Tienes 3 mascotas registradas. Nombres disponibles: Dappy y Nala."
    )


def test_registered_pets_keeps_total_count_independent_from_returned_names() -> None:
    handler = RegisteredPetsToolHandler(
        GetRegisteredPets(
            PetsRepository(
                RegisteredPetsDirectory(
                    total_count=12,
                    pets=(RegisteredPet("pet-1", "Dappy"),),
                )
            )
        )
    )

    result = handler(principal(), RegisteredPetsToolArguments())

    assert result.final_response == ("Tienes 12 mascotas registradas. Nombres disponibles: Dappy.")


def test_registered_pets_directory_rejects_duplicate_references() -> None:
    with pytest.raises(ValueError):
        RegisteredPetsDirectory(
            total_count=2,
            pets=(
                RegisteredPet("duplicate", "Dappy"),
                RegisteredPet("duplicate", "Nala"),
            ),
        )
