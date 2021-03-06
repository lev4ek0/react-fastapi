from io import BytesIO

import numpy as np
import requests
from aiogram import Dispatcher, Bot, types
from PIL import UnidentifiedImageError
import face_recognition
from retinaface import RetinaFace

from . import settings
from .service import get_url, process_photo_by_url

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("I can find amount of faces at the photo. "
                        "Just send me it or send me link.")


@dp.message_handler(content_types=['text', 'photo', 'document'])
async def handle_photos(message: types.Message):
    try:
        url = await get_url(message)
        f = requests.get(url)
        image = face_recognition.load_image_file(BytesIO(f.content))
        image_array = np.array(image)
        response = f'{RetinaFace.detect_faces(image_array)}'
    except requests.exceptions.MissingSchema:
        response = 'Url is wrong'
    except UnidentifiedImageError:
        response = 'File is not image'
    except Exception:
        response = 'Smth went wrong'
    await message.reply(response)


# @dp.message_handler(content_types=['text', 'photo', 'document'])
# async def handle_photos(message: types.Message):
#     try:
#         url = await get_url(message)
#         photo, amount_of_faces = process_photo_by_url(url)
#         response = f'Faces found: {amount_of_faces}'
#     except requests.exceptions.MissingSchema:
#         response = 'Url is wrong'
#     except UnidentifiedImageError:
#         response = 'File is not image'
#     except Exception:
#         response = 'Smth went wrong'
#     else:
#         return await message.reply_photo(
#             photo=photo,
#             caption=response
#         )
#     await message.reply(response)
