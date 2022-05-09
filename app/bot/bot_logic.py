from functools import lru_cache
from io import BytesIO

import requests
from aiogram import Dispatcher, Bot, types
import face_recognition
from PIL import UnidentifiedImageError

from . import settings

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("I can find amount of faces at the photo. "
                        "Just send me it or send me link.")


async def get_url(message: types.Message) -> str:
    url = message.text
    if len(message.photo) != 0:
        url = await message.photo[-1].get_url()
    if message.document is not None:
        url = await message.document.get_url()
    return url


@lru_cache
async def find_faces(url: str) -> int:
    f = requests.get(url)
    image = face_recognition.load_image_file(BytesIO(f.content))
    face_locations = face_recognition.face_locations(image)
    return len(face_locations)


@dp.message_handler(content_types=['text', 'photo', 'document'])
async def handle_photos(message: types.Message):
    url = await get_url(message)
    try:
        amount_of_faces = await find_faces(url)
        response = f'Faces found: {amount_of_faces}'
    except requests.exceptions.MissingSchema:
        response = f'Url is wrong'
    except UnidentifiedImageError:
        response = f'File is not image'
    await message.reply(response)
