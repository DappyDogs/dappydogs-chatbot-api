import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

import pytest

from dappydogs_chatbot_api.adapters.user_profiles import (
    FirestoreDogProfileRepository,
    LocalSnapshotDogProfileRepository,
)
from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.profile import ProfileLookupStatus
from dappydogs_chatbot_api.normalization.users import ProfileCatalogs, UserProfileNormalizer
from dappydogs_chatbot_api.ports.profile import ProfileSourceError


@pytest.fixture
def principal() -> AuthenticatedPrincipal:
    return AuthenticatedPrincipal(uid="verified-user", app_id="verified-app")


@pytest.fixture
def normalizer() -> UserProfileNormalizer:
    return UserProfileNormalizer(ProfileCatalogs.unverified())


def profile_fields() -> dict[str, object]:
    return {
        "userId": "verified-user",
        "dogName": "Dappy",
        "dogDate": "1577923200",
        "dogBreed": 7,
        "dogGender": 1,
        "email": "must-not-enter-domain@example.test",
        "deviceToken": "must-not-enter-domain",
    }


def write_snapshot(directory: Path, document_id: str, fields: Mapping[str, object]) -> None:
    payload = {
        "fields": dict(fields),
        "_firestore": {"path": f"Users/{document_id}"},
    }
    (directory / f"{document_id}.json").write_text(json.dumps(payload), encoding="utf-8")


def test_local_repository_reads_only_the_authenticated_document(
    tmp_path: Path,
    principal: AuthenticatedPrincipal,
    normalizer: UserProfileNormalizer,
) -> None:
    write_snapshot(tmp_path, "verified-user", profile_fields())
    write_snapshot(tmp_path, "different-user", profile_fields() | {"dogName": "Private"})
    repository = LocalSnapshotDogProfileRepository(tmp_path, normalizer)

    result = repository.get_for(principal)

    assert result.status is ProfileLookupStatus.FOUND
    assert result.profile is not None
    assert result.profile.name == "Dappy"
    assert "must-not-enter-domain" not in repr(result.profile)
    assert "Private" not in repr(result.profile)


def test_local_repository_returns_typed_not_found(
    tmp_path: Path,
    principal: AuthenticatedPrincipal,
    normalizer: UserProfileNormalizer,
) -> None:
    repository = LocalSnapshotDogProfileRepository(tmp_path, normalizer)

    result = repository.get_for(principal)

    assert result.status is ProfileLookupStatus.NOT_FOUND
    assert result.profile is None


def test_local_repository_rejects_path_traversal(
    tmp_path: Path, normalizer: UserProfileNormalizer
) -> None:
    repository = LocalSnapshotDogProfileRepository(tmp_path, normalizer)
    forged_principal = AuthenticatedPrincipal(uid="../outside", app_id="verified-app")

    with pytest.raises(ProfileSourceError):
        repository.get_for(forged_principal)


@pytest.mark.parametrize("payload", ["[]", "{}", '{"fields": []}', "not-json"])
def test_local_repository_rejects_malformed_snapshot_contracts(
    tmp_path: Path,
    principal: AuthenticatedPrincipal,
    normalizer: UserProfileNormalizer,
    payload: str,
) -> None:
    (tmp_path / "verified-user.json").write_text(payload, encoding="utf-8")
    repository = LocalSnapshotDogProfileRepository(tmp_path, normalizer)

    with pytest.raises(ProfileSourceError):
        repository.get_for(principal)


@dataclass
class FakeSnapshot:
    id: str
    exists: bool
    fields: Mapping[str, object] | None

    def to_dict(self) -> Mapping[str, object] | None:
        return self.fields


class FakeDocumentReference:
    def __init__(self, snapshot: FakeSnapshot) -> None:
        self._snapshot = snapshot

    def get(self) -> FakeSnapshot:
        return self._snapshot


class RecordingCollection:
    def __init__(self, snapshot: FakeSnapshot, calls: list[str]) -> None:
        self._snapshot = snapshot
        self._calls = calls

    def document(self, document_id: str) -> FakeDocumentReference:
        self._calls.append(document_id)
        return FakeDocumentReference(self._snapshot)


class RecordingFirestoreClient:
    def __init__(self, snapshot: FakeSnapshot) -> None:
        self.snapshot = snapshot
        self.collections: list[str] = []
        self.documents: list[str] = []

    def collection(self, collection_name: str) -> RecordingCollection:
        self.collections.append(collection_name)
        return RecordingCollection(self.snapshot, self.documents)


def test_firestore_repository_derives_the_path_only_from_the_principal(
    principal: AuthenticatedPrincipal,
    normalizer: UserProfileNormalizer,
) -> None:
    client = RecordingFirestoreClient(
        FakeSnapshot(id="verified-user", exists=True, fields=profile_fields())
    )
    repository = FirestoreDogProfileRepository(client, normalizer)

    result = repository.get_for(principal)

    assert result.status is ProfileLookupStatus.FOUND
    assert client.collections == ["Users"]
    assert client.documents == ["verified-user"]


def test_firestore_repository_wraps_provider_failures(
    principal: AuthenticatedPrincipal,
    normalizer: UserProfileNormalizer,
) -> None:
    class FailingClient:
        def collection(self, _collection_name: str) -> RecordingCollection:
            raise RuntimeError("sensitive provider detail")

    repository = FirestoreDogProfileRepository(FailingClient(), normalizer)

    with pytest.raises(ProfileSourceError, match="Profile source is unavailable") as captured:
        repository.get_for(principal)

    assert "sensitive provider detail" not in str(captured.value)


def test_firestore_repository_wraps_snapshot_materialization_failures(
    principal: AuthenticatedPrincipal,
    normalizer: UserProfileNormalizer,
) -> None:
    class FailingSnapshot(FakeSnapshot):
        def to_dict(self) -> Mapping[str, object] | None:
            raise RuntimeError("sensitive snapshot detail")

    client = RecordingFirestoreClient(FailingSnapshot(id="verified-user", exists=True, fields=None))
    repository = FirestoreDogProfileRepository(client, normalizer)

    with pytest.raises(ProfileSourceError, match="Profile source is unavailable") as captured:
        repository.get_for(principal)

    assert "sensitive snapshot detail" not in str(captured.value)
