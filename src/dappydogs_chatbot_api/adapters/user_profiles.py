import json
import logging
from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, cast

from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.profile import ProfileLookup, ProfileWarning
from dappydogs_chatbot_api.normalization.users import (
    LegacyUserProfileFields,
    UserProfileNormalizer,
)
from dappydogs_chatbot_api.ports.profile import ProfileSourceError

_logger = logging.getLogger("dappydogs_chatbot_api.profile_compatibility")


class FirestoreDocumentSnapshot(Protocol):
    @property
    def exists(self) -> bool: ...

    @property
    def id(self) -> str: ...

    def to_dict(self) -> Mapping[str, object] | None: ...


class FirestoreDocumentReference(Protocol):
    def get(self) -> FirestoreDocumentSnapshot: ...


class FirestoreCollectionReference(Protocol):
    def document(self, document_id: str) -> FirestoreDocumentReference: ...


class FirestoreClient(Protocol):
    def collection(self, collection_name: str) -> FirestoreCollectionReference: ...


class FirestoreDogProfileRepository:
    def __init__(self, client: FirestoreClient, normalizer: UserProfileNormalizer) -> None:
        self._client = client
        self._normalizer = normalizer

    def get_for(
        self,
        principal: AuthenticatedPrincipal,
        *,
        pet_name: str | None = None,
    ) -> ProfileLookup:
        try:
            snapshot = self._client.collection("Users").document(principal.uid).get()
            if not snapshot.exists:
                return ProfileLookup.not_found()
            fields = snapshot.to_dict()
        except Exception as error:
            raise ProfileSourceError("Profile source is unavailable") from error
        if fields is None:
            raise ProfileSourceError("Profile source returned no fields")
        lookup = self._normalize(snapshot.id, principal, fields)
        return _select_by_name(lookup, pet_name)

    def _normalize(
        self,
        document_id: str,
        principal: AuthenticatedPrincipal,
        fields: Mapping[str, object],
    ) -> ProfileLookup:
        profile = self._normalizer.normalize(
            document_id=document_id,
            principal_uid=principal.uid,
            fields=LegacyUserProfileFields.from_mapping(fields),
        )
        _log_warnings(profile.warnings)
        return ProfileLookup.found(profile)


class LocalSnapshotDogProfileRepository:
    def __init__(self, users_directory: Path, normalizer: UserProfileNormalizer) -> None:
        self._users_directory = users_directory.resolve()
        self._normalizer = normalizer

    def get_for(
        self,
        principal: AuthenticatedPrincipal,
        *,
        pet_name: str | None = None,
    ) -> ProfileLookup:
        path = (self._users_directory / f"{principal.uid}.json").resolve()
        if path.parent != self._users_directory:
            raise ProfileSourceError("Invalid profile document identifier")
        if not path.is_file():
            return ProfileLookup.not_found()
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ProfileSourceError("Profile snapshot has an invalid contract")
            raw_fields = payload.get("fields")
            if not isinstance(raw_fields, dict):
                raise ProfileSourceError("Profile snapshot has an invalid contract")
            fields = cast(dict[str, object], raw_fields)
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as error:
            raise ProfileSourceError("Profile snapshot is unavailable") from error
        profile = self._normalizer.normalize(
            document_id=path.stem,
            principal_uid=principal.uid,
            fields=LegacyUserProfileFields.from_mapping(fields),
        )
        _log_warnings(profile.warnings)
        return _select_by_name(ProfileLookup.found(profile), pet_name)


def _log_warnings(warnings: tuple[ProfileWarning, ...]) -> None:
    for warning in warnings:
        field = getattr(warning, "field", "unknown")
        issue = getattr(warning, "issue", "unknown")
        _logger.info("profile_compatibility_warning", extra={"field": field, "issue": issue})


def _select_by_name(lookup: ProfileLookup, pet_name: str | None) -> ProfileLookup:
    if pet_name is None or lookup.profile is None:
        return lookup
    stored_name = lookup.profile.name
    if stored_name is None or stored_name.strip().casefold() != pet_name.strip().casefold():
        return ProfileLookup.not_found()
    return lookup
