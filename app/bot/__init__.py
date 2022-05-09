from .. import config


settings = config.get_config("dev")
BASE_ROUTE = "bot"


def register_routes(app, root="api"):
    from .controller import router as bot_router

    app.include_router(bot_router, prefix=f"/{root}/{BASE_ROUTE}")
