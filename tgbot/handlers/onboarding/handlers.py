import asyncio
import logging

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler

from dtb import settings
import tgbot.handlers.onboarding.keyboards as keyboards
from classifier.models import ClassificationRequest
from users.models import User

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

    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"Hello, {user.tg_str}!\nTo classify a phone number, send /classify phone_number.\nExample: /classify +79151428383\nI will try to find the avatars of the phone number owner in Telegram and WhatsApp and calculate the average age of the person in the avatars, using computer vision.",
        parse_mode=ParseMode.HTML,
    )

    return ConversationHandler.END


def data_dict_to_str(data: dict):
    if data.get("url"):
        if not (data.get("age") or data.get("age_error")):
            return f"URL: <a href='{data.get('url')}'>avatar</a>\n"
        if data.get("age"):
            return f"Age: {data.get('age')}\nURL: <a href='{data.get('url')}'>avatar</a>\n"
        else:
            return f"Age: <code>{data['age_error']}</code>\nURL: <a href='{data.get('url')}'>avatar</a>\n"
    else:
        return f"Error: <code>{data.get('error')}</code>\n"


def classify(update: Update, context: CallbackContext):
    if len(update.message.text.split()) < 2:
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text=f"No phone number provided",
            parse_mode=ParseMode.HTML,
        )
        return

    phone = "".join(update.message.text.split()[1:])

    if not phone.startswith("+"):
        phone = "+" + phone

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

    try:
        telegram_data["url"] = asyncio.run(classifier.utils.telegram_get_avatar_url(phone_str))
    except Exception as e:
        telegram_data["error"] = str(e)

    message.edit_text(
        text=f"Classifying {phone_str}...\nCountry: {country}\n<b>Telegram</b>:\n{data_dict_to_str(telegram_data)}",
        parse_mode=ParseMode.HTML,
    )

    whatsapp_data = {}

    try:
        whatsapp_data["url"] = classifier.utils.whatsapp_get_avatar_url(phone_str)
    except Exception as e:
        whatsapp_data["error"] = str(e)

    message.edit_text(
        text=f"Classifying {phone_str}...\nCountry: {country}\n<b>Telegram</b>:\n{data_dict_to_str(telegram_data)}\n<b>WhatsApp</b>:\n{data_dict_to_str(whatsapp_data)}",
        parse_mode=ParseMode.HTML,
    )

    if telegram_data.get("url"):
        try:
            telegram_data["age"] = classifier.utils.get_age(telegram_data.get("url"))
        except Exception as e:
            telegram_data["age_error"] = str(e)

        message.edit_text(
            text=f"Classifying {phone_str}...\nCountry: {country}\n<b>Telegram</b>:\n{data_dict_to_str(telegram_data)}\n<b>WhatsApp</b>:\n{data_dict_to_str(whatsapp_data)}",
            parse_mode=ParseMode.HTML,
        )

    if whatsapp_data.get("url"):
        try:
            whatsapp_data["age"] = classifier.utils.get_age(whatsapp_data.get("url"))
        except Exception as e:
            whatsapp_data["age_error"] = str(e)

        message.edit_text(
            text=f"Classifying {phone_str}...\nCountry: {country}\n<b>Telegram</b>:\n{data_dict_to_str(telegram_data)}\n<b>WhatsApp</b>:\n{data_dict_to_str(whatsapp_data)}",
            parse_mode=ParseMode.HTML,
        )

    if whatsapp_data.get("age") and telegram_data.get("age"):
        average_age = whatsapp_data.get("age") + telegram_data.get("age") // 2
    elif whatsapp_data.get("age"):
        average_age = whatsapp_data.get("age")
    elif telegram_data.get("age"):
        average_age = telegram_data.get("age")
    else:
        average_age = "No enough data"

    classification_request = ClassificationRequest(
        user=User.get_user(update),
        phone=phone_str,
        country=country,
        telegram_age=telegram_data.get("age"),
        whatsapp_age=whatsapp_data.get("age"),
        telegram_avatar_url=telegram_data.get("url"),
        whatsapp_avatar_url=whatsapp_data.get("url"),
    )
    classification_request.save()

    message.edit_text(
        text=f"Phone: <code>{phone_str}</code>\nCountry: {country}\n<b>Telegram</b>:\n{data_dict_to_str(telegram_data)}\n<b>WhatsApp</b>:\n{data_dict_to_str(whatsapp_data)}\nAverage age: {average_age}",
        parse_mode=ParseMode.HTML,
    )
