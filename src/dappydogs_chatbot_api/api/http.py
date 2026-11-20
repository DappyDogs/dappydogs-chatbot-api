import asyncio
import json
import logging
from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from time import monotonic
from typing import Final
from uuid import uuid4

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

API_V1_PREFIX: Final = "/api/v1"
REQUEST_ID_HEADER: Final = b"x-request-id"

_request_id: ContextVar[str | None] = ContextVar("request_id", default=None)
_logger = logging.getLogger("dappydogs_chatbot_api.http")


class RequestBodyTooLargeError(BaseException):
    """Signal that the ASGI request stream exceeded its configured limit."""


class InvalidContentLengthError(BaseException):
    """Signal an ambiguous, malformed, or negative Content-Length value."""


class JsonLogFormatter(logging.Formatter):
    """Serialize the allowlisted HTTP log fields without request-controlled content."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "event": record.getMessage(),
            "level": record.levelname.lower(),
            "logger": record.name,
        }
        for field in (
            "request_id",
            "method",
            "route",
            "status_code",
            "duration_ms",
            "error_type",
        ):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def current_request_id() -> str | None:
    return _request_id.get()


def configure_json_logging() -> None:
    if any(getattr(handler, "_dappydogs_json", False) for handler in _logger.handlers):
        return
    handler = logging.StreamHandler()
    handler.setFormatter(JsonLogFormatter())
    handler._dappydogs_json = True  # type: ignore[attr-defined]
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)
    _logger.propagate = False


class HttpBoundaryMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        *,
        max_request_body_bytes: int,
        request_timeout_seconds: float,
    ) -> None:
        self._app = app
        self._max_request_body_bytes = max_request_body_bytes
        self._request_timeout_seconds = request_timeout_seconds
        configure_json_logging()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        request_id = uuid4().hex
        token = _request_id.set(request_id)
        scope.setdefault("state", {})["request_id"] = request_id
        started_at = monotonic()
        status_code = 500
        response_started = False

        async def tracked_send(message: Message) -> None:
            nonlocal response_started, status_code
            if message["type"] == "http.response.start":
                response_started = True
                status_code = message["status"]
                headers = list(message.get("headers", []))
                headers.append((REQUEST_ID_HEADER, request_id.encode("ascii")))
                message["headers"] = headers
            await send(message)

        limited_receive = self._limited_receive(receive)
        try:
            content_length = self._content_length(scope)
            if content_length is not None and content_length > self._max_request_body_bytes:
                await self._send_boundary_error(
                    tracked_send,
                    status_code=413,
                    code="request_too_large",
                    message="The request body is too large.",
                    request_id=request_id,
                )
            else:
                await asyncio.wait_for(
                    self._app(scope, limited_receive, tracked_send),
                    timeout=self._request_timeout_seconds,
                )
        except RequestBodyTooLargeError:
            if not response_started:
                await self._send_boundary_error(
                    tracked_send,
                    status_code=413,
                    code="request_too_large",
                    message="The request body is too large.",
                    request_id=request_id,
                )
        except InvalidContentLengthError:
            if not response_started:
                await self._send_boundary_error(
                    tracked_send,
                    status_code=400,
                    code="invalid_request",
                    message="The request is invalid.",
                    request_id=request_id,
                )
        except TimeoutError:
            if not response_started:
                await self._send_boundary_error(
                    tracked_send,
                    status_code=504,
                    code="request_timeout",
                    message="The request timed out.",
                    request_id=request_id,
                )
        except asyncio.CancelledError:
            status_code = 499
            raise
        except Exception as error:
            _logger.error(
                "request_failed",
                extra={"request_id": request_id, "error_type": type(error).__name__},
            )
            if not response_started:
                await self._send_boundary_error(
                    tracked_send,
                    status_code=500,
                    code="internal_error",
                    message="The operation could not be completed.",
                    request_id=request_id,
                )
        finally:
            self._log_completion(scope, request_id, status_code, started_at)
            _request_id.reset(token)

    def _limited_receive(self, receive: Receive) -> Receive:
        received = 0

        async def limited_receive() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self._max_request_body_bytes:
                    raise RequestBodyTooLargeError
            return message

        return limited_receive

    @staticmethod
    def _content_length(scope: Scope) -> int | None:
        values = [value for name, value in scope["headers"] if name == b"content-length"]
        if not values:
            return None
        if len(values) != 1:
            raise InvalidContentLengthError
        try:
            parsed = int(values[0])
        except ValueError:
            raise InvalidContentLengthError from None
        if parsed < 0:
            raise InvalidContentLengthError
        return parsed

    @staticmethod
    async def _send_boundary_error(
        send: Send,
        *,
        status_code: int,
        code: str,
        message: str,
        request_id: str,
    ) -> None:
        response = JSONResponse(
            status_code=status_code,
            content={"error": {"code": code, "message": message, "request_id": request_id}},
        )
        empty_receive: Callable[[], Awaitable[Message]] = _empty_receive
        await response({"type": "http"}, empty_receive, send)

    @staticmethod
    def _log_completion(scope: Scope, request_id: str, status_code: int, started_at: float) -> None:
        route = scope.get("route")
        route_path = getattr(route, "path", "unmatched")
        _logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": scope["method"],
                "route": route_path,
                "status_code": status_code,
                "duration_ms": round((monotonic() - started_at) * 1000, 3),
            },
        )


async def _empty_receive() -> Message:
    return {"type": "http.request", "body": b"", "more_body": False}
