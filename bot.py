import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bonjour ! Je suis Vis Assistant. Envoyez-moi un message."
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    await update.message.reply_text(
        f"Vous avez écrit : {user_message}"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    app.run_polling()


if __name__ == "__main__":
    main()
