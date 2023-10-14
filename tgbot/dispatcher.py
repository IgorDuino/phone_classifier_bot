from telegram.ext import (
    Dispatcher,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
)

from dtb.settings import DEBUG

from tgbot.main import bot
from tgbot.utils import error

from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers

from tgbot import states


def s(pattern) -> callable:
    def check(string):
        return string.startswith(pattern)

    return check


def setup_dispatcher(dp: Dispatcher):
    persistence = PicklePersistence(filename="conversations")
    dp.persistence = persistence

    dp.add_handler(CommandHandler("start", onboarding_handlers.start, pass_user_data=True))

    dp.add_handler(CommandHandler("classify", onboarding_handlers.classify, pass_user_data=True))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
