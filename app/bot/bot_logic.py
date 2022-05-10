import traceback
from functools import lru_cache
from io import BytesIO

import numpy as np
import requests
from aiogram import Dispatcher, Bot, types
import face_recognition
from PIL import UnidentifiedImageError, Image

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


def get_image(url: str):
    f = requests.get(url)
    image = face_recognition.load_image_file(BytesIO(f.content))
    return image


@lru_cache
def find_faces(url: str) -> int:
    image = get_image(url)
    face_locations = face_recognition.face_locations(image)
    return len(face_locations)


def lighting_image(img, coef):
    img = np.array(img) * coef
    return img.astype(np.uint8)


@lru_cache
def find_face(url: str):
    image = get_image(url)
    face_locations = face_recognition.face_locations(image)
    faces = []
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        faces.append((face_location, face_image))
    image = lighting_image(image, 0.5)
    for face in faces:
        top, right, bottom, left = face[0]
        image[top:bottom, left:right] = face[1]
    pil_image = Image.fromarray(image)
    return pil_image


@dp.message_handler(content_types=['text', 'photo', 'document'])
async def handle_photos(message: types.Message):
    url = await get_url(message)
    try:
        amount_of_faces = find_faces(url)
        face = find_face(url)
        response = f'Faces found: {amount_of_faces}'
        if face is not None:
            bytes_face = BytesIO()
            face.save(bytes_face, 'png')
            photo = bytes_face.getvalue()
            await message.reply_photo(photo=photo, caption=response)
    except requests.exceptions.MissingSchema:
        response = 'Url is wrong'
    except UnidentifiedImageError:
        response = 'File is not image'
    except Exception:
        response = f'Smth went wrong:{traceback.format_exc()}'
    await message.reply(response)
