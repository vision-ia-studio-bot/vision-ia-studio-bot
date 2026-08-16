import os
import requests

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
                    "Tu es Vis Assistant. Réponds en français, en anglais "
                    "ou en russe selon la langue utilisée."
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
