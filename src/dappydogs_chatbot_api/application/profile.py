from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any

from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.profile import (
    CatalogValue,
    DogProfile,
    ProfileLookupStatus,
)
from dappydogs_chatbot_api.ports.profile import DogProfileRepository, ProfileSourceError


class ProfileAttribute(StrEnum):
    NAME = "name"
    BIRTH_DATE = "birth_date"
    BREED = "breed"
    GENDER = "gender"
    SOCIABILITY = "sociability"
    ENERGY = "energy"


class ProfileCapabilityUnavailableError(Exception):
    """Signal a controlled profile dependency failure without source details."""


@dataclass(frozen=True, slots=True)
class ProfileQuery:
    attributes: tuple[ProfileAttribute, ...]

    def __post_init__(self) -> None:
        if not self.attributes:
            raise ValueError("at least one profile attribute is required")
        if len(self.attributes) != len(set(self.attributes)):
            raise ValueError("profile attributes must be unique")


class GetDogProfile:
    def __init__(self, repository: DogProfileRepository) -> None:
        self._repository = repository

    def execute(
        self,
        principal: AuthenticatedPrincipal,
        query: ProfileQuery,
    ) -> Mapping[str, Any]:
        try:
            lookup = self._repository.get_for(principal)
        except ProfileSourceError as error:
            raise ProfileCapabilityUnavailableError from error
        if lookup.status is ProfileLookupStatus.NOT_FOUND:
            return MappingProxyType({"status": "not_found", "fields": {}})
        if lookup.profile is None:
            raise RuntimeError("Found profile lookup has no profile")
        fields = {
            attribute.value: self._project(attribute, lookup.profile)
            for attribute in query.attributes
        }
        return MappingProxyType({"status": "found", "fields": fields})

    @staticmethod
    def _project(attribute: ProfileAttribute, profile: DogProfile) -> Mapping[str, Any]:
        if attribute is ProfileAttribute.NAME:
            return _optional_value(profile.name)
        if attribute is ProfileAttribute.BIRTH_DATE:
            if profile.birth_date is None:
                return _unavailable()
            return {
                "status": "available",
                "value": profile.birth_date.value.isoformat(),
                "precision": profile.birth_date.precision.value,
            }
        catalog_value = {
            ProfileAttribute.BREED: profile.breed,
            ProfileAttribute.GENDER: profile.gender,
            ProfileAttribute.SOCIABILITY: profile.sociability,
            ProfileAttribute.ENERGY: profile.energy,
        }[attribute]
        return _catalog_value(catalog_value)


def _optional_value(value: str | None) -> Mapping[str, Any]:
    if value is None:
        return _unavailable()
    return {"status": "available", "value": value}


def _catalog_value(value: CatalogValue | None) -> Mapping[str, Any]:
    if value is None:
        return _unavailable()
    if value.label is None:
        return {
            "status": "available",
            "value": value.code,
            "value_type": "catalog_code",
        }
    return {
        "status": "available",
        "value": value.label,
        "value_type": "catalog_label",
        "code": value.code,
    }


def _unavailable() -> Mapping[str, Any]:
    return {"status": "unavailable"}
