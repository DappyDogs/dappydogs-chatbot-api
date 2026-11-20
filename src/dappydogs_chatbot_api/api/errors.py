from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from starlette.exceptions import HTTPException as StarletteHTTPException

from dappydogs_chatbot_api.domain.errors import (
    ApplicationError,
    AuthenticationConfigurationError,
    AuthenticationRequiredError,
    InvalidAuthenticationError,
)


class PublicError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    request_id: str


class ErrorEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: PublicError


def error_response(
    request: Request,
    *,
    status_code: int,
    code: str,
    message: str,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    request_id = str(request.state.request_id)
    envelope = ErrorEnvelope(error=PublicError(code=code, message=message, request_id=request_id))
    return JSONResponse(
        status_code=status_code,
        content=envelope.model_dump(),
        headers=headers,
    )


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationError)
    async def handle_application_error(_request: Request, error: ApplicationError) -> JSONResponse:
        status_code = status.HTTP_400_BAD_REQUEST
        headers = None
        if isinstance(error, (AuthenticationRequiredError, InvalidAuthenticationError)):
            status_code = status.HTTP_401_UNAUTHORIZED
            headers = {"WWW-Authenticate": "Bearer"}
        elif isinstance(error, AuthenticationConfigurationError):
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return error_response(
            _request,
            status_code=status_code,
            code=error.code,
            message=error.public_message,
            headers=headers,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, _error: RequestValidationError
    ) -> JSONResponse:
        return error_response(
            request,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            code="invalid_request",
            message="The request is invalid.",
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(request: Request, error: StarletteHTTPException) -> JSONResponse:
        code = "not_found" if error.status_code == status.HTTP_404_NOT_FOUND else "http_error"
        message = (
            "The requested resource was not found."
            if error.status_code == status.HTTP_404_NOT_FOUND
            else "The HTTP request could not be completed."
        )
        safe_headers = None
        if error.headers is not None and "Allow" in error.headers:
            safe_headers = {"Allow": error.headers["Allow"]}
        return error_response(
            request,
            status_code=error.status_code,
            code=code,
            message=message,
            headers=safe_headers,
        )
