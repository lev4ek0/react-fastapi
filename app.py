import logging
import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types
from fastapi import FastAPI

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT')

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.post('/webhook')
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

