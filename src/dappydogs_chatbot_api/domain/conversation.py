from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass(frozen=True, slots=True)
class ToolCall:
    name: str
    arguments: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("tool name cannot be empty")
        object.__setattr__(self, "arguments", MappingProxyType(dict(self.arguments)))


@dataclass(frozen=True, slots=True)
class ConversationMessage:
    role: MessageRole
    content: str
    tool_name: str | None = None
    tool_calls: tuple[ToolCall, ...] = ()

    def __post_init__(self) -> None:
        if not self.content.strip() and not self.tool_calls:
            raise ValueError("message content cannot be empty")
        if self.role is MessageRole.TOOL and not self.tool_name:
            raise ValueError("tool messages require a tool name")
        if self.role is not MessageRole.TOOL and self.tool_name is not None:
            raise ValueError("only tool messages can have a tool name")
        if self.tool_calls and self.role is not MessageRole.ASSISTANT:
            raise ValueError("only assistant messages can contain tool calls")


@dataclass(frozen=True, slots=True)
class ModelUsage:
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

    def __post_init__(self) -> None:
        for value in (self.prompt_tokens, self.completion_tokens):
            if value is not None and value < 0:
                raise ValueError("token counts cannot be negative")


@dataclass(frozen=True, slots=True)
class ModelResponse:
    content: str | None = None
    tool_calls: tuple[ToolCall, ...] = ()
    usage: ModelUsage = ModelUsage()

    def __post_init__(self) -> None:
        if self.content is not None and not self.content.strip():
            raise ValueError("response content cannot be blank")
        if self.content is None and not self.tool_calls:
            raise ValueError("response requires content or at least one tool call")
