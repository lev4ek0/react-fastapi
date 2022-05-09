from io import BytesIO

import requests
from aiogram import Dispatcher, Bot, types
import face_recognition

from . import settings

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("I can find amount of faces at the photo. "
                        "Just send me it or send me link.")


def find_faces(url: str) -> int:
    f = requests.get(url)
    if f.status_code != 200:
        raise Exception
    image = face_recognition.load_image_file(BytesIO(f.content))
    face_locations = face_recognition.face_locations(image)
    return len(face_locations)


@dp.message_handler()
async def handle_photos(message: types.Message):
    url = message.text
    try:
        amount_of_faces = find_faces(url)
        await message.reply(
            f'Faces found: {amount_of_faces}'
        )
    except Exception:
        await message.reply(
            'Url is wrong'
        )


@dp.message_handler(content_types=['photo', 'document'])
async def handle_photos(message: types.Message):
    url = await message.photo[-1].get_url()
    amount_of_faces = find_faces(url)
    await message.reply(
        f'Faces found: {amount_of_faces}'
    )
