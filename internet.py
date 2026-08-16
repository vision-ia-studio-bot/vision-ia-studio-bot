import os
import requests

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


def search_web(query):
    if not GNEWS_API_KEY:
        return "❌ La variable GNEWS_API_KEY est introuvable."

    try:
        response = requests.get(
            "https://gnews.io/api/v4/search",
            params={
                "q": query,
                "max": 1,
                "apikey": GNEWS_API_KEY,
            },
            timeout=10,
        )

        data = response.json()

        if response.status_code != 200:
            return f"❌ GNews : {data}"

        articles = data.get("articles", [])

        if not articles:
            return "❌ Aucun résultat trouvé."

        article = articles[0]

        return (
            f"📰 {article.get('title', '')}\n\n"
            f"{article.get('description', '')}"
        )

    except Exception as e:
        return f"❌ Erreur : {e}"
