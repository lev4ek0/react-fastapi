from .bot.bot_logic import bot
from . import settings


async def startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != settings.WEBHOOK_URL:
        await bot.set_webhook(
            url=settings.WEBHOOK_URL
        )


async def shutdown():
    await bot.session.close()
