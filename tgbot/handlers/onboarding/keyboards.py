from typing import List
import time

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from users.models import User


def t(text: str) -> str:
    return f"{text}:{time.time()}"
