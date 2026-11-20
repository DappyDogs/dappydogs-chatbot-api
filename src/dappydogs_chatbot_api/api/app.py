from importlib.metadata import version

from fastapi import FastAPI

from dappydogs_chatbot_api.api.errors import register_error_handlers
from dappydogs_chatbot_api.api.health import router as health_router
from dappydogs_chatbot_api.api.http import HttpBoundaryMiddleware
from dappydogs_chatbot_api.application.authentication import AuthenticateRequest
from dappydogs_chatbot_api.settings import Settings, get_settings


def create_app(
    settings: Settings | None = None,
    authenticator: AuthenticateRequest | None = None,
) -> FastAPI:
    resolved_settings = settings or get_settings()
    app = FastAPI(
        title=resolved_settings.service_name,
        version=version("dappydogs-chatbot-api"),
        docs_url=None if resolved_settings.is_production else "/docs",
        redoc_url=None,
    )
    app.state.settings = resolved_settings
    app.state.authenticator = authenticator
    register_error_handlers(app)
    app.include_router(health_router)
    app.add_middleware(
        HttpBoundaryMiddleware,
        max_request_body_bytes=resolved_settings.max_request_body_bytes,
        request_timeout_seconds=resolved_settings.request_timeout_seconds,
    )
    return app


app = create_app()
