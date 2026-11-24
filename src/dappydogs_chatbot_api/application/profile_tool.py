import json
from collections.abc import Mapping
from typing import Any

from pydantic import Field, field_validator

from dappydogs_chatbot_api.application.profile import (
    GetDogProfile,
    ProfileAttribute,
    ProfileCapabilityUnavailableError,
    ProfileQuery,
)
from dappydogs_chatbot_api.application.text import safe_text
from dappydogs_chatbot_api.application.tools import (
    RegisteredTool,
    ToolArguments,
    ToolExecutionError,
    ToolResult,
)
from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal


class DogProfileToolArguments(ToolArguments):
    fields: tuple[ProfileAttribute, ...] = Field(min_length=1, max_length=len(ProfileAttribute))

    @field_validator("fields", mode="before")
    @classmethod
    def parse_json_encoded_fields(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return value
        return decoded

    @field_validator("fields")
    @classmethod
    def validate_unique_fields(
        cls, value: tuple[ProfileAttribute, ...]
    ) -> tuple[ProfileAttribute, ...]:
        if len(value) != len(set(value)):
            raise ValueError("fields must be unique")
        return value


class DogProfileToolHandler:
    def __init__(self, capability: GetDogProfile) -> None:
        self._capability = capability

    def __call__(
        self,
        principal: AuthenticatedPrincipal,
        arguments: DogProfileToolArguments,
    ) -> ToolResult:
        try:
            payload = self._capability.execute(principal, ProfileQuery(arguments.fields))
        except ProfileCapabilityUnavailableError as error:
            raise ToolExecutionError from error
        return ToolResult(
            payload=payload, final_response=_render_response(payload, arguments.fields)
        )


def build_dog_profile_tool(capability: GetDogProfile) -> RegisteredTool[DogProfileToolArguments]:
    return RegisteredTool(
        name="get_dog_profile",
        description=(
            "Return only the requested dog profile fields for the authenticated user. "
            "A catalogue field with value_type catalog_code is available and its numeric "
            "value must be reported exactly without qualifying it as missing or unregistered."
        ),
        arguments_type=DogProfileToolArguments,
        handler=DogProfileToolHandler(capability),
    )


def _render_response(payload: Mapping[str, Any], fields: tuple[ProfileAttribute, ...]) -> str:
    if payload.get("status") == "not_found":
        return "No hay un perfil de perro registrado para tu cuenta."
    raw_fields = payload.get("fields")
    if not isinstance(raw_fields, Mapping):
        raise ToolExecutionError
    sentences = [_render_field(field, raw_fields.get(field.value)) for field in fields]
    return " ".join(sentences)


def _render_field(field: ProfileAttribute, raw_value: object) -> str:
    if not isinstance(raw_value, Mapping):
        raise ToolExecutionError
    value = raw_value.get("value")
    if raw_value.get("status") == "unavailable":
        return {
            ProfileAttribute.NAME: "El nombre de tu perro no está registrado.",
            ProfileAttribute.BIRTH_DATE: "La fecha de nacimiento de tu perro no está registrada.",
            ProfileAttribute.BREED: "La raza de tu perro no está registrada.",
            ProfileAttribute.GENDER: "El sexo de tu perro no está registrado.",
            ProfileAttribute.SOCIABILITY: "La sociabilidad de tu perro no está registrada.",
            ProfileAttribute.ENERGY: "El nivel de energía de tu perro no está registrado.",
        }[field]
    if field is ProfileAttribute.NAME and isinstance(value, str):
        return f"Tu perro se llama {safe_text(value)}."
    if field is ProfileAttribute.BIRTH_DATE and isinstance(value, str):
        if raw_value.get("precision") == "year":
            return f"El año de nacimiento registrado de tu perro es {value[:4]}."
        return f"La fecha de nacimiento registrada de tu perro es {value}."
    if raw_value.get("value_type") == "catalog_code" and isinstance(value, int):
        sentence_start = {
            ProfileAttribute.BREED: "La raza de tu perro está registrada",
            ProfileAttribute.GENDER: "El sexo de tu perro está registrado",
            ProfileAttribute.SOCIABILITY: "La sociabilidad de tu perro está registrada",
            ProfileAttribute.ENERGY: "El nivel de energía de tu perro está registrado",
        }.get(field)
        if sentence_start is not None:
            return f"{sentence_start} con el código {value}."
    if raw_value.get("value_type") == "catalog_label" and isinstance(value, str):
        subject = {
            ProfileAttribute.BREED: "La raza de tu perro",
            ProfileAttribute.GENDER: "El sexo de tu perro",
            ProfileAttribute.SOCIABILITY: "La sociabilidad de tu perro",
            ProfileAttribute.ENERGY: "El nivel de energía de tu perro",
        }.get(field)
        if subject is not None:
            return f"{subject} es {safe_text(value)}."
    raise ToolExecutionError
