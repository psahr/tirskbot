import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TULLA_PATTERN = re.compile(
    r'\b(tu(?:len|let|lee|lemme|lette|levat|li|lin|lit|li|limme|litte|livat|lla|len|'
    r'les|lla|llut|lisi|lisin|lisit|lisi|lisimme|lisitte|lisivat|liko|'
    r'letko|lisiko|leeko|llaanko|lisinko|lkaa|lkoot|ltava|u|un|'
    r'ut|uks|llaan|utte|ltiin))\b',
    re.IGNORECASE
)

GENERAL_THREAD_ID = None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    logger.info(f"Message received — chat_id: {message.chat_id}, thread_id: {message.message_thread_id}, text: {message.text!r}")

    thread_id = message.message_thread_id
    if thread_id != GENERAL_THREAD_ID:
        logger.info(f"Ignoring message — thread_id {thread_id} is not General ({GENERAL_THREAD_ID})")
        return

    text = message.text or ""
    if TULLA_PATTERN.search(text):
        logger.info("Pattern matched, sending reply")
        await context.bot.send_message(
            chat_id=message.chat_id,
            text="Tirsk",
            message_thread_id=GENERAL_THREAD_ID
        )

def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
