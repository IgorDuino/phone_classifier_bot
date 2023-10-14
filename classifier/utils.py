from pyrogram import Client
from pyrogram.types import InputPhoneContact
from dtb import settings
import requests
from django.urls import reverse
import os

app = Client(
    "account", api_id=settings.API_ID, api_hash=settings.API_HASH, workdir=os.path.join(settings.BASE_DIR, "classifier")
)
app.start()


def telegram_get_avatar_url(phone: str) -> bytes:
    app.import_contacts([InputPhoneContact(phone, phone)])
    avatar = app.download_media(app.get_chat_photos(phone).__next__(), in_memory=True)

    file_name = os.path.join(settings.BASE_DIR, "classifier/safe_folder", f"{phone}.png")
    with open(file_name, "wb") as f:
        f.write(bytes(avatar.getbuffer()))

    return reverse("download_file", args=[file_name])


def whatsapp_get_avatar_url(phone: str):
    url = f"https://whatsapp-data1.p.rapidapi.com/number/{phone}"

    headers = {
        "X-RapidAPI-Key": "53b8c82477msh8a6ad862de88525p125eafjsn0d6e73261f8e",
        "X-RapidAPI-Host": "whatsapp-data1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)

    return response.json().get("profilePic")


def get_age(image_url: str, accuracy_boost=3):
    url = "https://face-detection6.p.rapidapi.com/img/face-age-gender"

    payload = {"url": image_url, "accuracy_boost": accuracy_boost}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": settings.RAPID_KEY,
        "X-RapidAPI-Host": "face-detection6.p.rapidapi.com",
    }

    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    age_range = response["detected_faces"][0]["Age"]["Age-Range"]
    avg = (age_range["Low"] + age_range["High"]) // 2

    return avg
