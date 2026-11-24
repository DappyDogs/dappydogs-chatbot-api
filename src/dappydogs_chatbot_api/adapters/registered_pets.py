from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.pets import RegisteredPet, RegisteredPetsDirectory
from dappydogs_chatbot_api.domain.profile import DogProfile, ProfileLookupStatus
from dappydogs_chatbot_api.ports.pets import RegisteredPetsSourceError
from dappydogs_chatbot_api.ports.profile import DogProfileRepository, ProfileSourceError


class EmbeddedProfileRegisteredPetsRepository:
    """Expose the current embedded dog profile through the multi-pet port."""

    def __init__(self, profile_repository: DogProfileRepository) -> None:
        self._profile_repository = profile_repository

    def list_for(self, principal: AuthenticatedPrincipal) -> RegisteredPetsDirectory:
        try:
            lookup = self._profile_repository.get_for(principal)
        except ProfileSourceError as error:
            raise RegisteredPetsSourceError from error
        if lookup.status is ProfileLookupStatus.NOT_FOUND or lookup.profile is None:
            return RegisteredPetsDirectory(total_count=0, pets=())
        if not _contains_pet_data(lookup.profile):
            return RegisteredPetsDirectory(total_count=0, pets=())
        pet = RegisteredPet(reference="primary", name=lookup.profile.name)
        return RegisteredPetsDirectory(total_count=1, pets=(pet,))


def _contains_pet_data(profile: DogProfile) -> bool:
    return any(
        value is not None
        for value in (
            profile.name,
            profile.birth_date,
            profile.breed,
            profile.gender,
            profile.sociability,
            profile.energy,
        )
    )
