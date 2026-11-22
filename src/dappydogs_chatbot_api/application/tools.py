import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from dappydogs_chatbot_api.domain.authentication import AuthenticatedPrincipal
from dappydogs_chatbot_api.domain.conversation import ToolCall
from dappydogs_chatbot_api.ports.model import ModelTool


class ToolArguments(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


type ToolHandler[ArgumentsT: ToolArguments] = Callable[
    [AuthenticatedPrincipal, ArgumentsT], Mapping[str, Any]
]


class ToolRegistryError(Exception):
    """Base error for rejected model-requested tool execution."""


class UnknownToolError(ToolRegistryError):
    pass


class InvalidToolArgumentsError(ToolRegistryError):
    pass


class InvalidToolResultError(ToolRegistryError):
    pass


@dataclass(frozen=True, slots=True)
class PreparedToolCall:
    execute: Callable[[AuthenticatedPrincipal], Mapping[str, Any]]


@dataclass(frozen=True, slots=True)
class RegisteredTool[ArgumentsT: ToolArguments]:
    name: str
    description: str
    arguments_type: type[ArgumentsT]
    handler: ToolHandler[ArgumentsT]

    def model_contract(self) -> ModelTool:
        return ModelTool(
            name=self.name,
            description=self.description,
            parameters=self.arguments_type.model_json_schema(),
        )


class ToolRegistry:
    def __init__(
        self,
        version: str,
        tools: tuple[RegisteredTool[Any], ...] = (),
        *,
        max_result_bytes: int = 32_768,
    ) -> None:
        if not version.strip():
            raise ValueError("registry version cannot be empty")
        if max_result_bytes < 1:
            raise ValueError("max_result_bytes must be positive")
        by_name: dict[str, RegisteredTool[Any]] = {}
        for tool in tools:
            if not tool.name.strip() or tool.name in by_name:
                raise ValueError("tool names must be non-empty and unique")
            if not tool.description.strip():
                raise ValueError("tool descriptions cannot be empty")
            by_name[tool.name] = tool
        self._version = version
        self._tools = MappingProxyType(by_name)
        self._max_result_bytes = max_result_bytes

    @property
    def version(self) -> str:
        return self._version

    def model_contracts(self) -> tuple[ModelTool, ...]:
        return tuple(tool.model_contract() for tool in self._tools.values())

    def prepare(self, call: ToolCall) -> PreparedToolCall:
        tool = self._tools.get(call.name)
        if tool is None:
            raise UnknownToolError
        try:
            validated = tool.arguments_type.model_validate(call.arguments)
        except ValidationError as error:
            raise InvalidToolArgumentsError from error
        return PreparedToolCall(execute=lambda principal: tool.handler(principal, validated))

    def execute(self, principal: AuthenticatedPrincipal, prepared: PreparedToolCall) -> str:
        result = prepared.execute(principal)
        try:
            serialized = json.dumps(
                dict(result), ensure_ascii=False, separators=(",", ":"), sort_keys=True
            )
        except (TypeError, ValueError) as error:
            raise InvalidToolResultError from error
        if len(serialized.encode("utf-8")) > self._max_result_bytes:
            raise InvalidToolResultError
        return serialized
