from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from dappydogs_chatbot_api.domain.profile import (
    BirthDatePrecision,
    CatalogStatus,
    CatalogValue,
    DataIssue,
    DogBirthDate,
    DogProfile,
    ProfileField,
    ProfileWarning,
)

PROFILE_SOURCE_FIELDS: Final = frozenset(
    {
        "userId",
        "dogName",
        "dogDate",
        "dogBreed",
        "dogGender",
        "dogSociability",
        "dogEnergy",
    }
)


class LegacyValueState(StrEnum):
    MISSING = "missing"
    NULL = "null"
    EMPTY = "empty"
    PRESENT = "present"


@dataclass(frozen=True, slots=True)
class LegacyValue:
    state: LegacyValueState
    value: object | None = None


@dataclass(frozen=True, slots=True)
class LegacyUserProfileFields:
    values: Mapping[str, LegacyValue]

    @classmethod
    def from_mapping(cls, fields: Mapping[str, object]) -> LegacyUserProfileFields:
        selected: dict[str, LegacyValue] = {}
        for name in PROFILE_SOURCE_FIELDS:
            if name not in fields:
                selected[name] = LegacyValue(LegacyValueState.MISSING)
                continue
            value = fields[name]
            if value is None:
                selected[name] = LegacyValue(LegacyValueState.NULL)
            elif isinstance(value, str) and not value.strip():
                selected[name] = LegacyValue(LegacyValueState.EMPTY)
            else:
                selected[name] = LegacyValue(LegacyValueState.PRESENT, value)
        return cls(values=MappingProxyType(selected))


@dataclass(frozen=True, slots=True)
class ProfileCatalogs:
    breeds: Mapping[int, str]
    genders: Mapping[int, str]
    sociability: Mapping[int, str]
    energy: Mapping[int, str]

    def __post_init__(self) -> None:
        for field in ("breeds", "genders", "sociability", "energy"):
            source = getattr(self, field)
            normalized: dict[int, str] = {}
            for code, label in source.items():
                if isinstance(code, bool) or not isinstance(code, int):
                    raise ValueError(f"{field} codes must be integers")
                if not isinstance(label, str) or not label.strip():
                    raise ValueError(f"{field} labels must be non-empty strings")
                normalized[code] = label.strip()
            object.__setattr__(self, field, MappingProxyType(normalized))

    @classmethod
    def unverified(cls) -> ProfileCatalogs:
        empty: Mapping[int, str] = MappingProxyType({})
        return cls(breeds=empty, genders=empty, sociability=empty, energy=empty)


class UserProfileNormalizer:
    def __init__(
        self,
        catalogs: ProfileCatalogs,
        *,
        today: date | None = None,
        maximum_dog_age_years: int = 30,
    ) -> None:
        if maximum_dog_age_years <= 0:
            raise ValueError("maximum_dog_age_years must be positive")
        self._catalogs = catalogs
        self._today = today or date.today()
        self._minimum_birth_year = self._today.year - maximum_dog_age_years

    def normalize(
        self,
        *,
        document_id: str,
        principal_uid: str,
        fields: LegacyUserProfileFields,
    ) -> DogProfile:
        warnings: list[ProfileWarning] = []
        if document_id != principal_uid:
            warnings.append(ProfileWarning(ProfileField.DOCUMENT_ID, DataIssue.INCONSISTENT))
        self._check_user_id(fields.values["userId"], principal_uid, warnings)

        name = self._string(fields.values["dogName"], ProfileField.DOG_NAME, warnings)
        birth_date = self._birth_date(fields.values["dogDate"], warnings)
        breed = self._catalog(
            fields.values["dogBreed"], ProfileField.DOG_BREED, self._catalogs.breeds, warnings
        )
        gender = self._catalog(
            fields.values["dogGender"],
            ProfileField.DOG_GENDER,
            self._catalogs.genders,
            warnings,
        )
        sociability = self._catalog(
            fields.values["dogSociability"],
            ProfileField.DOG_SOCIABILITY,
            self._catalogs.sociability,
            warnings,
        )
        energy = self._catalog(
            fields.values["dogEnergy"],
            ProfileField.DOG_ENERGY,
            self._catalogs.energy,
            warnings,
        )
        return DogProfile(
            name=name,
            birth_date=birth_date,
            breed=breed,
            gender=gender,
            sociability=sociability,
            energy=energy,
            warnings=tuple(warnings),
        )

    @staticmethod
    def _issue_for(value: LegacyValue) -> DataIssue:
        return {
            LegacyValueState.MISSING: DataIssue.MISSING,
            LegacyValueState.NULL: DataIssue.NULL,
            LegacyValueState.EMPTY: DataIssue.EMPTY,
            LegacyValueState.PRESENT: DataIssue.INVALID,
        }[value.state]

    def _check_user_id(
        self, value: LegacyValue, principal_uid: str, warnings: list[ProfileWarning]
    ) -> None:
        if value.state is not LegacyValueState.PRESENT:
            warnings.append(ProfileWarning(ProfileField.USER_ID, self._issue_for(value)))
        elif not isinstance(value.value, str) or value.value != principal_uid:
            warnings.append(ProfileWarning(ProfileField.USER_ID, DataIssue.INCONSISTENT))

    def _string(
        self,
        value: LegacyValue,
        field: ProfileField,
        warnings: list[ProfileWarning],
    ) -> str | None:
        if value.state is not LegacyValueState.PRESENT:
            warnings.append(ProfileWarning(field, self._issue_for(value)))
            return None
        if not isinstance(value.value, str):
            warnings.append(ProfileWarning(field, DataIssue.INVALID))
            return None
        normalized = value.value.strip()
        if not normalized:
            warnings.append(ProfileWarning(field, DataIssue.EMPTY))
            return None
        return normalized

    def _birth_date(
        self, value: LegacyValue, warnings: list[ProfileWarning]
    ) -> DogBirthDate | None:
        field = ProfileField.DOG_BIRTH_DATE
        raw = self._string(value, field, warnings)
        if raw is None:
            return None
        if not raw.isascii() or not raw.isdigit():
            warnings.append(ProfileWarning(field, DataIssue.INVALID))
            return None
        try:
            if len(raw) == 4:
                year = int(raw)
                parsed = date(year, 1, 1)
                precision = BirthDatePrecision.YEAR
            elif len(raw) in {9, 10}:
                parsed = datetime.fromtimestamp(int(raw), tz=UTC).date()
                precision = BirthDatePrecision.DAY
            else:
                warnings.append(ProfileWarning(field, DataIssue.INVALID))
                return None
        except OverflowError, ValueError, OSError:
            warnings.append(ProfileWarning(field, DataIssue.INVALID))
            return None
        if not self._minimum_birth_year <= parsed.year <= self._today.year:
            warnings.append(ProfileWarning(field, DataIssue.INVALID))
            return None
        if parsed > self._today:
            warnings.append(ProfileWarning(field, DataIssue.INVALID))
            return None
        return DogBirthDate(value=parsed, precision=precision)

    def _catalog(
        self,
        value: LegacyValue,
        field: ProfileField,
        labels: Mapping[int, str],
        warnings: list[ProfileWarning],
    ) -> CatalogValue | None:
        if value.state is not LegacyValueState.PRESENT:
            warnings.append(ProfileWarning(field, self._issue_for(value)))
            return None
        if isinstance(value.value, bool) or not isinstance(value.value, int):
            warnings.append(ProfileWarning(field, DataIssue.INVALID))
            return None
        label = labels.get(value.value)
        if label is None:
            warnings.append(ProfileWarning(field, DataIssue.UNKNOWN_CATALOG_VALUE))
            return CatalogValue(code=value.value, label=None, status=CatalogStatus.UNKNOWN)
        return CatalogValue(code=value.value, label=label, status=CatalogStatus.MAPPED)
