from datetime import datetime, timedelta
import logging
import re

from dtb import settings

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler
from tgbot import states
import tgbot.handlers.onboarding.keyboards as keyboards

from users.models import User
import asyncio

import classifier.utils

from phone_iso3166.country import phone_country
import phonenumbers

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    user = User.get_user(update)
    if user:
        created = False
    else:
        if settings.DISABLE_FOR_NEW_USERS:
            context.bot.send_message(
                chat_id=update.effective_user.id,
                text="Отключена регистрация новых пользователей",
                parse_mode=ParseMode.HTML,
            )
            return
        user = User(
            user_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
        )
        user.save()
        created = True

    if created:
        start_code = update.message.text.split(" ")[1] if len(update.message.text.split(" ")) > 1 else None
        if start_code:
            referrer = User.objects.filter(user_id=start_code).first()
            if referrer:
                user.deep_link = start_code

    user.is_active = True
    user.save()

    context.user_data.clear()

    return ConversationHandler.END


def classify(update: Update, context: CallbackContext):
    phone = update.message.text.split()[1]

    try:
        phone = phonenumbers.parse(phone, None)
    except:
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=f"Invalid phone number",
            parse_mode=ParseMode.HTML,
        )
        return

    phone_str = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)

    message = context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"Start *classifying* <b>asd</b> {phone_str}...",
        parse_mode=ParseMode.HTML,
    )

    country = "Unrecognized"

    from phone_iso3166.country import phone_country
    import pycountry

    c = pycountry.countries.get(alpha_2=phone_country(phone_str))
    if c:
        country = c.name

    message.edit_text(
        text=f"Classifying {phone_str}...\nCountry: {country}",
    )

    telegram_data = {}

    telegram_data["url"] = asyncio.run(classifier.utils.telegram_get_avatar_url(phone_str))

    whatsapp_data = {}

    whatsapp_data["url"] = classifier.utils.whatsapp_get_avatar_url(phone_str)

    if telegram_data.get("url"):
        telegram_data["age"] = classifier.utils.get_age(telegram_data.get("url"))

    if whatsapp_data.get("url"):
        whatsapp_data["age"] = classifier.utils.get_age(whatsapp_data.get("url"))

    if whatsapp_data.get("age") and telegram_data.get("age"):
        average_age = whatsapp_data.get("age") + telegram_data.get("age") / 2
    elif whatsapp_data.get("age"):
        average_age = whatsapp_data.get("age")
    elif telegram_data.get("age"):
        average_age = telegram_data.get("age")
    else:
        average_age = "Unrecognized"

    message.edit_text(
        text=f"Phone: {phone}\nCountry: {country}\nTelegram: {telegram_data}\nWhatsapp: {whatsapp_data}\nAverage age: {average_age}",
        parse_mode=ParseMode.HTML,
    )
