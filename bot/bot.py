import pandas as pd
import requests as rq
import vnstock as stock
import logging
import traceback
import html
import json
import telegram
from telegram import (
    Update,
    User,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    AIORateLimiter,
    filters
)
from telegram.constants import ParseMode, ChatAction
import config

logger = logging.getLogger(__name__)

HELP_MESSAGE = """Commands:
⚪ /settings – Show settings
⚪ /balance – Show balance
⚪ /help – Show help
"""

def split_text_into_chunks(text, chunk_size):
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]

async def help_handle(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.HTML)

async def error_handle(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    try:
        # collect error message
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = "".join(tb_list)
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            f"An exception was raised while handling an update\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

        # split text into multiple messages due to 4096 character limit
        for message_chunk in split_text_into_chunks(message, 4096):
            try:
                await context.bot.send_message(update.effective_chat.id, message_chunk, parse_mode=ParseMode.HTML)
            except telegram.error.BadRequest:
                # answer has invalid characters, so we send it without parse_mode
                await context.bot.send_message(update.effective_chat.id, message_chunk)
    except:
        await context.bot.send_message(update.effective_chat.id, "Some error in error handler")

async def menu_init(application: Application):
    await application.bot.set_my_commands([
        BotCommand("/new", "Start new dialog"),
        BotCommand("/overview", "Overview"),
        BotCommand("/help", "Show help message"),
    ])

def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(config.telegram_token)
        .concurrent_updates(True)
        .rate_limiter(AIORateLimiter(max_retries=5))
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .post_init(menu_init)
        .build()
    )
        # add handlers
    user_filter = filters.ALL
    if len(config.allowed_telegram_usernames) > 0:
        usernames = [x for x in config.allowed_telegram_usernames if isinstance(x, str)]
        any_ids = [x for x in config.allowed_telegram_usernames if isinstance(x, int)]
        user_ids = [x for x in any_ids if x > 0]
        group_ids = [x for x in any_ids if x < 0]
        user_filter = filters.User(username=usernames) | filters.User(user_id=user_ids) | filters.Chat(chat_id=group_ids)

    application.add_handler(CommandHandler("help", help_handle, filters=user_filter))

    application.add_error_handler(error_handle)

    # start the bot
    application.run_polling()


if __name__ == "__main__":
    run_bot()
