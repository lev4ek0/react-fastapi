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


@dp.message_handler(content_types=['photo', 'document', 'text'])
async def handle_photos(message: types.Message):
    print(message.text)
    if len(message.photo) != 0:
        url = message.photo[-1].get_url()
        print(url)
    if message.document is not None:
        url = message.document.get_url()
        print(url)
    await message.reply(
        f'Faces found: {1}'
    )


# def find_faces(url: str) -> int:
#     f = requests.get(url)
#     if f.status_code != 200:
#         raise Exception
#     image = face_recognition.load_image_file(BytesIO(f.content))
#     face_locations = face_recognition.face_locations(image)
#     return len(face_locations)
#
#
# @dp.message_handler()
# async def handle_urls(message: types.Message):
#     url = message.text
#     try:
#         amount_of_faces = find_faces(url)
#         await message.reply(
#             f'Faces found: {amount_of_faces}'
#         )
#     except requests.exceptions.MissingSchema:
#         await message.reply(
#             f'Url is wrong'
#         )
#     except UnidentifiedImageError:
#         await message.reply(
#             f'File is not image'
#         )
#
#
# @dp.message_handler(content_types=['photo'])
# async def handle_photos(message: types.Message):
#     url = await message.photo[-1].get_url()
#     amount_of_faces = find_faces(url)
#     await message.reply(
#         f'Faces found: {amount_of_faces}'
#     )
#
#
# @dp.message_handler(content_types=['document'])
# async def handle_documents(message: types.Message):
#     try:
#         url = await message.document.get_url()
#         amount_of_faces = find_faces(url)
#         await message.reply(
#             f'Faces found: {amount_of_faces}'
#         )
#     except UnidentifiedImageError:
#         await message.reply(
#             f'File is not image'
#         )
