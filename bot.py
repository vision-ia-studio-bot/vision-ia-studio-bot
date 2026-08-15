import os
import requests
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

memory = {}

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_ai(message):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es Vis Assistant. Réponds dans la langue du message "
                    "(français, anglais ou russe)."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30,
        )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception:
        return "Désolé, le service d'IA est momentanément indisponible."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bonjour ! Je suis Vis Assistant."
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append(
        {
            "role": "user",
            "content": message,
        }
    )

    answer = ask_ai(message)

    memory[user_id].append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    memory[user_id] = memory[user_id][-10:]

    await update.message.reply_text(answer)

if __name__ == "__main__":
    main()
