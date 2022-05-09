from io import BytesIO

from aiogram import Dispatcher, Bot, types
import face_recognition

from . import settings

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


@dp.message_handler(content_types=['photo'])
async def handle_photos(message: types.Message):
    file = await message.photo[-1].get_url()
    image = face_recognition.load_image_file(BytesIO(file))
    face_locations = face_recognition.face_locations(image)
    await message.answer(
        f'Size: {message.photo[-1].file_size}\n'
        f'\"Лиц найдено:\", {len(face_locations)}'
    )
