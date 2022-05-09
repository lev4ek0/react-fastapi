from aiogram import Dispatcher, Bot, types

from . import settings

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    print(message)
    await message.answer(message.text)
