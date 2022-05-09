from fastapi import FastAPI

from .bot.bot_logic import bot
from .config import get_config
from .routes import register_routes


def create_app(config="dev"):
    settings = get_config(config=config)

    app = FastAPI(title="Bot API")

    register_routes(app)

    @app.on_event('startup')
    async def on_startup():
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != settings.WEBHOOK_URL:
            await bot.set_webhook(
                url=settings.WEBHOOK_URL
            )

    @app.on_event('shutdown')
    async def on_shutdown():
        await bot.session.close()

    return app
