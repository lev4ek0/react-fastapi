from aiogram import Dispatcher, Bot, types

from app import get_config


settings = get_config("dev")
bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
