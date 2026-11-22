from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class BirthDatePrecision(StrEnum):
    DAY = "day"
    YEAR = "year"


class CatalogStatus(StrEnum):
    MAPPED = "mapped"
    UNKNOWN = "unknown"


class ProfileField(StrEnum):
    DOCUMENT_ID = "document_id"
    USER_ID = "user_id"
    DOG_NAME = "dog_name"
    DOG_BIRTH_DATE = "dog_birth_date"
    DOG_BREED = "dog_breed"
    DOG_GENDER = "dog_gender"
    DOG_SOCIABILITY = "dog_sociability"
    DOG_ENERGY = "dog_energy"


class DataIssue(StrEnum):
    MISSING = "missing"
    NULL = "null"
    EMPTY = "empty"
    INVALID = "invalid"
    INCONSISTENT = "inconsistent"
    UNKNOWN_CATALOG_VALUE = "unknown_catalog_value"


@dataclass(frozen=True, slots=True)
class ProfileWarning:
    field: ProfileField
    issue: DataIssue


@dataclass(frozen=True, slots=True)
class DogBirthDate:
    value: date
    precision: BirthDatePrecision


@dataclass(frozen=True, slots=True)
class CatalogValue:
    code: int
    label: str | None
    status: CatalogStatus


@dataclass(frozen=True, slots=True)
class DogProfile:
    name: str | None
    birth_date: DogBirthDate | None
    breed: CatalogValue | None
    gender: CatalogValue | None
    sociability: CatalogValue | None
    energy: CatalogValue | None
    warnings: tuple[ProfileWarning, ...]


class ProfileLookupStatus(StrEnum):
    FOUND = "found"
    NOT_FOUND = "not_found"


@dataclass(frozen=True, slots=True)
class ProfileLookup:
    status: ProfileLookupStatus
    profile: DogProfile | None

    def __post_init__(self) -> None:
        if (self.status is ProfileLookupStatus.FOUND) is (self.profile is None):
            raise ValueError("Profile lookup status and value are inconsistent")

    @classmethod
    def found(cls, profile: DogProfile) -> ProfileLookup:
        return cls(status=ProfileLookupStatus.FOUND, profile=profile)

    @classmethod
    def not_found(cls) -> ProfileLookup:
        return cls(status=ProfileLookupStatus.NOT_FOUND, profile=None)
