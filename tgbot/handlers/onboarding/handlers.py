from datetime import datetime, timedelta
import logging
import re

from dtb import settings

from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler
from tgbot import states
import tgbot.handlers.onboarding.keyboards as keyboards

from users.models import User


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
