from .model import Widget  # noqa
from .schema import WidgetSchema  # noqa
from .. import get_config

BASE_ROUTE = "bot"
settings = get_config(config="dev")


def register_routes(app, root="api"):
    from .controller import router as bot_router

    app.include_router(bot_router, prefix=f"/{root}/{BASE_ROUTE}")
