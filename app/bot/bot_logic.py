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


def get_image(url):
    f = requests.get(url)
    image = face_recognition.load_image_file(BytesIO(f.content))
    return image


def get_face_locations(image):
    face_locations = face_recognition.face_locations(image)
    return face_locations


def get_faces(image, face_locations):
    faces = []
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        faces.append((face_location, face_image))
    return faces


def darken_image(img, coef):
    img = np.array(img) * coef
    return img.astype(np.uint8)


def add_objects_to_photo(objects, image):
    for _ in objects:
        top, right, bottom, left = _[0]
        image[top:bottom, left:right] = _[1]


def find_face(image, face_locations):
    faces = get_faces(image=image, face_locations=face_locations)
    if faces:
        image = darken_image(image, 0.5)
    add_objects_to_photo(objects=faces, image=image)
    pil_image = Image.fromarray(image)
    return pil_image


@lru_cache
def process_photo_by_url(url):
    image = get_image(url=url)
    face_locations = get_face_locations(image=image)
    amount_of_faces = len(face_locations)
    face = find_face(image=image, face_locations=face_locations)
    bytes_face = BytesIO()
    face.save(bytes_face, 'png')
    photo = bytes_face.getvalue()
    return photo, amount_of_faces


@dp.message_handler(content_types=['text', 'photo', 'document'])
async def handle_photos(message: types.Message):
    url = await get_url(message)
    try:
        photo, amount_of_faces = process_photo_by_url(url)
        response = f'Faces found: {amount_of_faces}'
    except requests.exceptions.MissingSchema:
        response = 'Url is wrong'
    except UnidentifiedImageError:
        response = 'File is not image'
    except Exception:
        response = f'Smth went wrong:{traceback.format_exc()}'
    else:
        return await message.reply_photo(photo=photo, caption=response)
    await message.reply(response)
