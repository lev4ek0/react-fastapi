import logging
import os

from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from fastapi import FastAPI

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
SECRET = os.getenv('SECRET')
WEBHOOK_PATH = f'/webhook/{SECRET}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'


logging.basicConfig(level=logging.INFO)

app = FastAPI()


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


@app.on_event('startup')
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(f'/{WEBHOOK_PATH}')
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event('shutdown')
async def on_shutdown():
    await bot.session.close()
