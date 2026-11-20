from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipal:
    """Authoritative identity derived exclusively from verified server-side evidence."""

    uid: str
    app_id: str

    def __post_init__(self) -> None:
        if not self.uid or not self.uid.strip():
            raise ValueError("uid cannot be empty")
        if not self.app_id or not self.app_id.strip():
            raise ValueError("app_id cannot be empty")
