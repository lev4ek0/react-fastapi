from fastapi import APIRouter
from aiogram import types, Dispatcher, Bot

from bot_logic import dp, bot
from . import settings

router = APIRouter()


@router.post(f'/{settings.WEBHOOK_PATH}')
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)
