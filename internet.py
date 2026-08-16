import os
import requests

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


def search_web(query):
    try:
        response = requests.get(
            "https://gnews.io/api/v4/search",
            params={
                "q": query,
                "lang": "fr",
                "max": 1,
                "apikey": GNEWS_API_KEY,
            },
            timeout=10,
        )

        if response.status_code != 200:
            return (
                f"Erreur GNews : "
                f"{response.status_code}"
            )

        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            return "Aucun résultat trouvé."

        article = articles[0]

        title = article.get("title", "")
        description = article.get("description", "")
        source = article.get("source", {}).get(
            "name",
            "Source inconnue",
        )

        return (
            f"📰 {title}\n\n"
            f"{description}\n\n"
            f"Source : {source}"
        )

    except Exception as e:
        return f"Erreur : {str(e)}"
