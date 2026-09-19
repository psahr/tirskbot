import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("telegram_bot")

TULLA_PATTERN = re.compile(
    r'\b(tu(?:len|let|lee|lemme|lette|levat|li|lin|lit|li|limme|litte|livat|lla|len|'
    r'les|lla|llut|lisi|lisin|lisit|lisi|lisimme|lisitte|lisivat|liko|'
    r'letko|lisiko|leeko|llaanko|lisinko|lkaa|lkoot|ltava|u|un|'
    r'ut|uks|llaan|utte|ltiin|utko|letko|uksä|utsä|leeks|leekse|ukkos|uksää|lisitko|uppa|leppa|uppas))\b',
    re.IGNORECASE
)

GENERAL_THREAD_ID = None


def get_sender_name(message):
    """Palauttaa lähettäjän nimen, tai UID:n jos nimeä ei ole saatavilla."""
    user = message.from_user

    if not user:
        return "tuntematon"

    name_parts = [
        user.first_name,
        user.last_name,
    ]

    name = " ".join(part for part in name_parts if part).strip()

    if name:
        return name

    if user.username:
        return f"@{user.username}"

    return f"uid={user.id}"


def get_chat_name(message):
    """Palauttaa ryhmän nimen, tai ID:n jos nimeä ei ole saatavilla."""
    chat = message.chat

    if chat.title:
        return chat.title

    if chat.username:
        return f"@{chat.username}"

    return f"id={chat.id}"


def log_message(message, status):
    """Kirjoittaa yhden selkeän lokirivin."""
    sender = get_sender_name(message)
    chat = get_chat_name(message)
    text = message.text or ""

    logger.info(
        "[%s] ryhmä=%s | lähettäjä=%s | viesti=%r",
        status,
        chat,
        sender,
        text
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    # Lokitus: ei muutosta varsinaiseen käsittelylogiikkaan.
    log_message(message, "VASTAANOTETTU")

    thread_id = message.message_thread_id
    if thread_id != GENERAL_THREAD_ID:
        log_message(message, "OHITETTU: väärä thread")
        return

    text = message.text or ""
    if TULLA_PATTERN.search(text):
        log_message(message, "VASTATAAN")

        await context.bot.send_message(
            chat_id=message.chat_id,
            text="Tirsk",
            message_thread_id=GENERAL_THREAD_ID
        )
    else:
        log_message(message, "OHITETTU: ei osumaa")


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]

    app = ApplicationBuilder().token(token).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
