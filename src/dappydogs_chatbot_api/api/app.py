from importlib.metadata import version

from fastapi import FastAPI

from dappydogs_chatbot_api.api.errors import register_error_handlers
from dappydogs_chatbot_api.api.health import router as health_router
from dappydogs_chatbot_api.settings import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    app = FastAPI(
        title=resolved_settings.service_name,
        version=version("dappydogs-chatbot-api"),
        docs_url=None if resolved_settings.is_production else "/docs",
        redoc_url=None,
    )
    app.state.settings = resolved_settings
    register_error_handlers(app)
    app.include_router(health_router)
    return app


app = create_app()
