from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from dappydogs_chatbot_api.domain.errors import ApplicationError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationError)
    async def handle_application_error(_request: Request, error: ApplicationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": {"code": error.code, "message": error.public_message}},
        )
