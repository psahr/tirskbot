import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TULLA_PATTERN = re.compile(
    r'\b(tul(?:en|et|ee|emme|ette|evat|i|in|it|i|imme|itte|ivat|la|le|len|'
    r'les|lla|lut|lisi|lisin|lisit|lisi|lisimme|lisitte|lisivat|ko|'
    r'teko|etko|isiko|eeko|laanko|isinko|kaa|koot|tava|tavan|tavaa|'
    r'tavalle|tavalta|taville|tavilta|tavilleen))\b',
    re.IGNORECASE
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if TULLA_PATTERN.search(text):
        await update.message.reply_text("Tirsk")

def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
