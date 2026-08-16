import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from ai import ask_ai
from memory import save_message, get_history

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bonjour ! Je suis Vis Assistant."
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    save_message(user_id, "user", message)

    history = get_history(user_id)

    context_text = "\n".join(
        f"{item['role']}: {item['content']}"
        for item in history
    )

    answer = ask_ai(context_text)

    save_message(user_id, "assistant", answer)

    await update.message.reply_text(answer)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply,
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
