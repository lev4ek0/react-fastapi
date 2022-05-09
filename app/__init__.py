from fastapi import FastAPI

from .bot.bot_logic import bot
from .bot.controller import router
from .start_app import startup


def create_app():
    app = FastAPI(title="Bot API")

    app.include_router(router, prefix=f"/api/bot")

    startup()

    @app.on_event('shutdown')
    async def on_shutdown():
        await bot.session.close()

    return app
