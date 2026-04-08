import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TULLA_PATTERN = re.compile(
    r'\b(tu(?:len|let|lee|lemme|lette|levat|li|lin|lit|li|limme|litte|livat|lla|len|'
    r'les|lla|llut|lisi|lisin|lisit|lisi|lisimme|lisitte|lisivat|liko|'
    r'letko|lisiko|leeko|llaanko|lisinko|lkaa|lkoot|ltava|u|un|'
    r'ut|uks|llaan|utte|ltiin))\b',
    re.IGNORECASE
)

GENERAL_THREAD_ID = 1  # Change this if your General topic has a different ID

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    # Only handle messages in the General thread/topic
    thread_id = message.message_thread_id
    if thread_id != GENERAL_THREAD_ID:
        return

    text = message.text or ""
    if TULLA_PATTERN.search(text):
        # Reply in the same thread by passing message_thread_id
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
