from fastapi import APIRouter
from aiogram import types, Dispatcher, Bot

from . import settings
from .bot_logic import dp, bot

router = APIRouter()


@router.post(settings.WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)
