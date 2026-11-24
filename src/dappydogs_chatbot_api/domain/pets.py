from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisteredPet:
    reference: str
    name: str | None

    def __post_init__(self) -> None:
        if not self.reference.strip():
            raise ValueError("pet reference cannot be empty")


@dataclass(frozen=True, slots=True)
class RegisteredPetsDirectory:
    total_count: int
    pets: tuple[RegisteredPet, ...]

    def __post_init__(self) -> None:
        if self.total_count < 0:
            raise ValueError("total_count cannot be negative")
        if self.total_count < len(self.pets):
            raise ValueError("total_count cannot be smaller than returned pets")
        references = tuple(pet.reference for pet in self.pets)
        if len(references) != len(set(references)):
            raise ValueError("pet references must be unique")
