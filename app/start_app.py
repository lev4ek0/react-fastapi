from .bot.bot_logic import bot
from .config import get_config

settings = get_config()


def startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != settings.WEBHOOK_URL:
        await bot.set_webhook(
            url=settings.WEBHOOK_URL
        )
