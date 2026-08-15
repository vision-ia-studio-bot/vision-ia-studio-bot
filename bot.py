import os
import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")


def ask_ai(prompt):
    url = "https://api-inference.huggingface.co/models/Qwen/Qwen3-4B-Instruct-2507"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": prompt
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60,
    )

    data = response.json()

    if isinstance(data, list):
        return data[0].get("generated_text", "Je n'ai pas pu générer de réponse.")

    return "Le service d'IA est momentanément indisponible."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bonjour ! Je suis Vis Assistant. Posez-moi une question."
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text

    answer = ask_ai(question)

    await update.message.reply_text(answer)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
