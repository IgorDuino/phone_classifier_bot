from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from users.models import User


def admin_privileges(func):
    def wrapper(update: Update, context: CallbackContext):
        u = User.get_user(update)
        if not u.is_admin:
            update.message.reply_text("Нет прав")
            return
        return func(update, context)

    return wrapper


@admin_privileges
def admin(update: Update, context: CallbackContext) -> None:
    """Show help info about all secret admins commands"""
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Админ",
        parse_mode=ParseMode.HTML,
    )
