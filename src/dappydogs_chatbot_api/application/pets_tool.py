from collections.abc import Mapping, Sequence
from typing import Any

from dappydogs_chatbot_api.application.pets import (
    GetRegisteredPets,
    RegisteredPetsUnavailableError,
)
from dappydogs_chatbot_api.application.text import safe_text
from dappydogs_chatbot_api.application.tools import (
    RegisteredTool,
    ToolArguments,
    ToolExecutionError,
    ToolResult,
)
from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal


class RegisteredPetsToolArguments(ToolArguments):
    pass


class RegisteredPetsToolHandler:
    def __init__(self, capability: GetRegisteredPets) -> None:
        self._capability = capability

    def __call__(
        self,
        principal: AuthenticatedPrincipal,
        arguments: RegisteredPetsToolArguments,
    ) -> ToolResult:
        del arguments
        try:
            payload = self._capability.execute(principal)
        except RegisteredPetsUnavailableError as error:
            raise ToolExecutionError from error
        return ToolResult(payload=payload, final_response=_render_registered_pets(payload))


def build_registered_pets_tool(
    capability: GetRegisteredPets,
) -> RegisteredTool[RegisteredPetsToolArguments]:
    return RegisteredTool(
        name="get_registered_pets",
        description=(
            "Return the number of pets registered for the authenticated user and the "
            "names that are available. Use it for existence, count, listing, and pet "
            "selection questions."
        ),
        arguments_type=RegisteredPetsToolArguments,
        handler=RegisteredPetsToolHandler(capability),
    )


def _render_registered_pets(payload: Mapping[str, Any]) -> str:
    count = payload.get("count")
    raw_pets = payload.get("pets")
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise ToolExecutionError
    if not isinstance(raw_pets, Sequence) or isinstance(raw_pets, str | bytes):
        raise ToolExecutionError
    if len(raw_pets) > count:
        raise ToolExecutionError
    names = _available_names(raw_pets)
    if count == 0:
        return "No tienes ninguna mascota registrada."
    if count == 1:
        if names:
            return f"Tienes una mascota registrada: {names[0]}."
        return "Tienes una mascota registrada."
    count_sentence = f"Tienes {count} mascotas registradas."
    if not names:
        return count_sentence
    return f"{count_sentence} Nombres disponibles: {_join_names(names)}."


def _available_names(raw_pets: Sequence[object]) -> tuple[str, ...]:
    names = []
    for raw_pet in raw_pets:
        if not isinstance(raw_pet, Mapping):
            raise ToolExecutionError
        name = raw_pet.get("name")
        if name is not None:
            if not isinstance(name, str):
                raise ToolExecutionError
            names.append(safe_text(name))
    return tuple(names)


def _join_names(names: tuple[str, ...]) -> str:
    if len(names) == 1:
        return names[0]
    return f"{', '.join(names[:-1])} y {names[-1]}"
