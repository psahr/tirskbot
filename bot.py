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
