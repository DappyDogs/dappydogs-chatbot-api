from datetime import date

import pytest

from dappydogs_chatbot_api.application.profile import (
    GetDogProfile,
    ProfileAttribute,
    ProfileCapabilityUnavailableError,
    ProfileQuery,
)
from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.profile import (
    BirthDatePrecision,
    CatalogStatus,
    CatalogValue,
    DogBirthDate,
    DogProfile,
    ProfileLookup,
)
from dappydogs_chatbot_api.ports.profile import ProfileSourceError


class RecordingRepository:
    def __init__(self, result: ProfileLookup) -> None:
        self._result = result
        self.principals: list[AuthenticatedPrincipal] = []
        self.pet_names: list[str | None] = []

    def get_for(
        self,
        principal: AuthenticatedPrincipal,
        *,
        pet_name: str | None = None,
    ) -> ProfileLookup:
        self.principals.append(principal)
        self.pet_names.append(pet_name)
        return self._result


def principal() -> AuthenticatedPrincipal:
    return AuthenticatedPrincipal(uid="verified-user", app_id="verified-app")


def complete_profile() -> DogProfile:
    return DogProfile(
        name="Dappy",
        birth_date=DogBirthDate(date(2020, 1, 2), BirthDatePrecision.DAY),
        breed=CatalogValue(7, None, CatalogStatus.UNKNOWN),
        gender=CatalogValue(1, "male", CatalogStatus.MAPPED),
        sociability=None,
        energy=CatalogValue(3, None, CatalogStatus.UNKNOWN),
        warnings=(),
    )


def test_profile_capability_projects_only_requested_fields() -> None:
    repository = RecordingRepository(ProfileLookup.found(complete_profile()))
    capability = GetDogProfile(repository)

    result = capability.execute(
        principal(), ProfileQuery((ProfileAttribute.NAME, ProfileAttribute.BREED))
    )

    assert result == {
        "status": "found",
        "fields": {
            "name": {"status": "available", "value": "Dappy"},
            "breed": {
                "status": "available",
                "value": 7,
                "value_type": "catalog_code",
            },
        },
    }
    assert repository.principals == [principal()]
    assert "gender" not in result["fields"]


def test_profile_capability_preserves_unavailable_and_mapped_states() -> None:
    capability = GetDogProfile(RecordingRepository(ProfileLookup.found(complete_profile())))

    result = capability.execute(
        principal(),
        ProfileQuery(
            (
                ProfileAttribute.BIRTH_DATE,
                ProfileAttribute.GENDER,
                ProfileAttribute.SOCIABILITY,
                ProfileAttribute.ENERGY,
            )
        ),
    )

    assert result == {
        "status": "found",
        "fields": {
            "birth_date": {
                "status": "available",
                "value": "2020-01-02",
                "precision": "day",
            },
            "gender": {
                "status": "available",
                "value": "male",
                "value_type": "catalog_label",
                "code": 1,
            },
            "sociability": {"status": "unavailable"},
            "energy": {
                "status": "available",
                "value": 3,
                "value_type": "catalog_code",
            },
        },
    }


def test_profile_capability_returns_typed_not_found() -> None:
    capability = GetDogProfile(RecordingRepository(ProfileLookup.not_found()))

    result = capability.execute(principal(), ProfileQuery((ProfileAttribute.NAME,)))

    assert result == {"status": "not_found", "fields": {}}


def test_profile_capability_translates_source_failure() -> None:
    class FailingRepository:
        def get_for(
            self,
            authenticated: AuthenticatedPrincipal,
            *,
            pet_name: str | None = None,
        ) -> ProfileLookup:
            del authenticated
            del pet_name
            raise ProfileSourceError("sensitive source detail")

    capability = GetDogProfile(FailingRepository())

    with pytest.raises(ProfileCapabilityUnavailableError) as captured:
        capability.execute(principal(), ProfileQuery((ProfileAttribute.NAME,)))

    assert str(captured.value) == ""


@pytest.mark.parametrize(
    "attributes",
    [(), (ProfileAttribute.NAME, ProfileAttribute.NAME)],
)
def test_profile_query_rejects_empty_or_duplicate_attributes(
    attributes: tuple[ProfileAttribute, ...],
) -> None:
    with pytest.raises(ValueError):
        ProfileQuery(attributes)


def test_profile_capability_passes_named_pet_selection_to_repository() -> None:
    repository = RecordingRepository(ProfileLookup.found(complete_profile()))
    capability = GetDogProfile(repository)

    capability.execute(
        principal(),
        ProfileQuery((ProfileAttribute.BREED,), pet_name="Nala"),
    )

    assert repository.pet_names == ["Nala"]
