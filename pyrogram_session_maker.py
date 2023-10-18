from pyrogram import Client
from decouple import config

app = Client("account", phone_number=config("PHONE_NUMBER"), api_id=config("API_ID"), api_hash=config("API_HASH"), workdir="tgsessions")

app.start()