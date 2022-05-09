from aiogram import Dispatcher, Bot, types

from . import settings

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(content_types=['photo'])
async def handle_photos(message: types.Message):
    await message.answer(str(message.photo[-1].file_size))
