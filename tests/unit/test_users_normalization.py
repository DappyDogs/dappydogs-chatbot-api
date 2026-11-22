import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import cast

import pytest

from dappydogs_chatbot_api.domain.profile import (
    BirthDatePrecision,
    CatalogStatus,
    DataIssue,
    ProfileField,
    ProfileLookup,
    ProfileLookupStatus,
)
from dappydogs_chatbot_api.normalization.users import (
    LegacyUserProfileFields,
    LegacyValueState,
    ProfileCatalogs,
    UserProfileNormalizer,
)


@pytest.fixture
def catalogs() -> ProfileCatalogs:
    return ProfileCatalogs(
        breeds={7: "example breed"},
        genders={1: "example gender"},
        sociability={2: "example sociability"},
        energy={3: "example energy"},
    )


@pytest.fixture
def normalizer(catalogs: ProfileCatalogs) -> UserProfileNormalizer:
    return UserProfileNormalizer(catalogs, today=date(2026, 11, 22))


def complete_fields(*, dog_date: str = "1577923200") -> dict[str, object]:
    return {
        "userId": "verified-user",
        "dogName": "  Dappy  ",
        "dogDate": dog_date,
        "dogBreed": 7,
        "dogGender": 1,
        "dogSociability": 2,
        "dogEnergy": 3,
    }


def test_raw_contract_distinguishes_missing_null_empty_and_present() -> None:
    fields = LegacyUserProfileFields.from_mapping({"dogName": "", "dogDate": None, "dogBreed": 7})

    assert fields.values["userId"].state is LegacyValueState.MISSING
    assert fields.values["dogName"].state is LegacyValueState.EMPTY
    assert fields.values["dogDate"].state is LegacyValueState.NULL
    assert fields.values["dogBreed"].state is LegacyValueState.PRESENT


def test_equivalent_platform_documents_produce_the_same_minimal_profile(
    normalizer: UserProfileNormalizer,
) -> None:
    ios = complete_fields() | {
        "so": "platform-a",
        "userImage": "private-owner-image",
        "email": "private@example.test",
        "latitude": 40.0,
        "friendList": ["private-friend"],
    }
    android = complete_fields() | {
        "os": "platform-b",
        "imageURL": "private-owner-image",
        "deviceToken": "private-device-token",
        "isSubscribed": 1,
        "walkingStartAt": "private-walk-state",
    }

    ios_profile = normalizer.normalize(
        document_id="verified-user",
        principal_uid="verified-user",
        fields=LegacyUserProfileFields.from_mapping(ios),
    )
    android_profile = normalizer.normalize(
        document_id="verified-user",
        principal_uid="verified-user",
        fields=LegacyUserProfileFields.from_mapping(android),
    )

    assert ios_profile == android_profile
    assert ios_profile.name == "Dappy"
    assert ios_profile.breed is not None
    assert ios_profile.breed.label == "example breed"
    assert ios_profile.warnings == ()
    serialized = repr(ios_profile)
    assert "private" not in serialized
    assert "email" not in serialized
    assert "latitude" not in serialized


@pytest.mark.parametrize(
    ("raw", "expected", "precision"),
    [
        ("2020", date(2020, 1, 1), BirthDatePrecision.YEAR),
        (
            str(int(datetime(2000, 1, 1, tzinfo=UTC).timestamp())),
            date(2000, 1, 1),
            BirthDatePrecision.DAY,
        ),
        (
            str(int(datetime(2020, 1, 2, tzinfo=UTC).timestamp())),
            date(2020, 1, 2),
            BirthDatePrecision.DAY,
        ),
    ],
)
def test_birth_date_supports_year_and_epoch_variants_without_inventing_precision(
    normalizer: UserProfileNormalizer,
    raw: str,
    expected: date,
    precision: BirthDatePrecision,
) -> None:
    profile = normalizer.normalize(
        document_id="verified-user",
        principal_uid="verified-user",
        fields=LegacyUserProfileFields.from_mapping(complete_fields(dog_date=raw)),
    )

    assert profile.birth_date is not None
    assert profile.birth_date.value == expected
    assert profile.birth_date.precision is precision


@pytest.mark.parametrize("raw", ["null", "123", "9999999999999", "1890", "100000000"])
def test_ambiguous_or_implausible_birth_dates_remain_unknown(
    normalizer: UserProfileNormalizer, raw: str
) -> None:
    profile = normalizer.normalize(
        document_id="verified-user",
        principal_uid="verified-user",
        fields=LegacyUserProfileFields.from_mapping(complete_fields(dog_date=raw)),
    )

    assert profile.birth_date is None
    assert (ProfileField.DOG_BIRTH_DATE, DataIssue.INVALID) in {
        (warning.field, warning.issue) for warning in profile.warnings
    }


def test_unknown_catalog_values_are_explicit_and_not_inferred(
    normalizer: UserProfileNormalizer,
) -> None:
    fields = complete_fields()
    fields["dogBreed"] = 999

    profile = normalizer.normalize(
        document_id="verified-user",
        principal_uid="verified-user",
        fields=LegacyUserProfileFields.from_mapping(fields),
    )

    assert profile.breed is not None
    assert profile.breed.code == 999
    assert profile.breed.label is None
    assert profile.breed.status is CatalogStatus.UNKNOWN
    assert ProfileField.DOG_BREED in {
        warning.field
        for warning in profile.warnings
        if warning.issue is DataIssue.UNKNOWN_CATALOG_VALUE
    }


def test_inconsistent_identifiers_are_reported_without_changing_ownership(
    normalizer: UserProfileNormalizer,
) -> None:
    fields = complete_fields()
    fields["userId"] = "different-user"

    profile = normalizer.normalize(
        document_id="verified-user",
        principal_uid="verified-user",
        fields=LegacyUserProfileFields.from_mapping(fields),
    )

    assert (ProfileField.USER_ID, DataIssue.INCONSISTENT) in {
        (warning.field, warning.issue) for warning in profile.warnings
    }


def test_all_observed_profile_schema_signatures_have_anonymized_fixtures(
    normalizer: UserProfileNormalizer,
) -> None:
    fixture_path = Path(__file__).parents[1] / "fixtures" / "users" / "profile_variants.json"
    fixtures = cast(list[dict[str, object]], json.loads(fixture_path.read_text(encoding="utf-8")))

    assert len(fixtures) == 7
    assert sum(cast(int, fixture["observed_count"]) for fixture in fixtures) == 898
    for fixture in fixtures:
        fields = cast(dict[str, object], fixture["fields"])
        profile = normalizer.normalize(
            document_id="verified-user",
            principal_uid="verified-user",
            fields=LegacyUserProfileFields.from_mapping(fields),
        )

        serialized = repr(profile)
        assert "excluded@example.test" not in serialized
        assert "excluded-token" not in serialized


def test_catalogs_are_immutable_copies() -> None:
    source = {1: " one "}
    catalogs = ProfileCatalogs(source, {}, {}, {})
    source[1] = "changed"

    assert catalogs.breeds[1] == "one"
    with pytest.raises(TypeError):
        catalogs.breeds[1] = "forbidden"  # type: ignore[index]


@pytest.mark.parametrize(
    "catalog",
    [{True: "invalid"}, {1: ""}, {1: "   "}],
)
def test_catalogs_reject_invalid_contracts(catalog: dict[object, str]) -> None:
    with pytest.raises(ValueError):
        ProfileCatalogs(catalog, {}, {}, {})  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("status", "has_profile"),
    [
        (ProfileLookupStatus.FOUND, False),
        (ProfileLookupStatus.NOT_FOUND, True),
    ],
)
def test_profile_lookup_rejects_inconsistent_state(
    normalizer: UserProfileNormalizer,
    status: ProfileLookupStatus,
    has_profile: bool,
) -> None:
    profile = normalizer.normalize(
        document_id="verified-user",
        principal_uid="verified-user",
        fields=LegacyUserProfileFields.from_mapping(complete_fields()),
    )

    with pytest.raises(ValueError):
        ProfileLookup(status=status, profile=profile if has_profile else None)
