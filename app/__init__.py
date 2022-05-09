from fastapi import FastAPI

from .bot.bot_logic import bot
from .bot.controller import router
from .fastapi_init import startup, shutdown
from .config import get_config

settings = get_config()


def create_app():
    app = FastAPI(
        title='Bot API',
        on_startup=[startup],
        on_shutdown=[shutdown]
    )

    app.include_router(router, prefix=f'/{settings.API_V1_STR}/bot')

    return app
