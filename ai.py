import os
import requests
from datetime import datetime

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_ai(message):
    url = "https://openrouter.ai/api/v1/chat/completions"

    today = datetime.now().strftime("%d/%m/%Y")

    system_prompt = f"""
Tu es Vis Assistant.

Date actuelle : {today}.

Règles :

- Réponds dans la langue utilisée par l'utilisateur.
- Utilise le contexte de la conversation.
- Si des informations récentes sont fournies dans le contexte, utilise-les.
- N'invente jamais une date ou un événement récent.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
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
        return (
            "Désolé, le service d'IA est momentanément indisponible."
        )
