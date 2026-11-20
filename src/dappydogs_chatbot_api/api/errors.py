from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from dappydogs_chatbot_api.domain.errors import (
    ApplicationError,
    AuthenticationConfigurationError,
    AuthenticationRequiredError,
    InvalidAuthenticationError,
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
        return JSONResponse(
            status_code=status_code,
            content={"error": {"code": error.code, "message": error.public_message}},
            headers=headers,
        )
