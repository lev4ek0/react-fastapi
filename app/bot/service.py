from functools import lru_cache
from io import BytesIO

import numpy as np
import requests
from aiogram import types
from PIL import Image
import face_recognition


async def get_url(message: types.Message) -> str:
    url = message.text
    if len(message.photo) != 0:
        url = await message.photo[-1].get_url()
    if message.document is not None:
        url = await message.document.get_url()
    return url


def _get_image(url):
    f = requests.get(url)
    image = face_recognition.load_image_file(BytesIO(f.content))
    return image


def _get_face_locations(image):
    face_locations = face_recognition.face_locations(image)
    return face_locations


def _get_faces(image, face_locations):
    faces = []
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        faces.append((face_location, face_image))
    return faces


def _darken_image(img, coef):
    img = np.array(img) * coef
    return img.astype(np.uint8)


def _add_objects_to_photo(objects, image):
    for _ in objects:
        top, right, bottom, left = _[0]
        image[top:bottom, left:right] = _[1]


def _find_face(image, face_locations):
    faces = _get_faces(image=image, face_locations=face_locations)
    if faces:
        image = _darken_image(image, 0.5)
    _add_objects_to_photo(objects=faces, image=image)
    pil_image = Image.fromarray(image)
    return pil_image


@lru_cache
def process_photo_by_url(url):
    image = _get_image(url=url)
    face_locations = _get_face_locations(image=image)
    face = _find_face(image=image, face_locations=face_locations)
    bytes_face = BytesIO()
    face.save(bytes_face, 'png')
    photo = bytes_face.getvalue()
    amount_of_faces = len(face_locations)
    return photo, amount_of_faces
