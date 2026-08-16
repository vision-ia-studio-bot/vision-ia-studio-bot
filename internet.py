import os
import requests

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")


def search_web(query):
    if not GNEWS_API_KEY:
        return None

    try:
        response = requests.get(
            "https://gnews.io/api/v4/search",
            params={
                "q": query,
                "max": 3,
                "apikey": GNEWS_API_KEY,
            },
            timeout=10,
        )

        if response.status_code != 200:
            return None

        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            return None

        results = []

        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            source = article.get(
                "source",
                {},
            ).get(
                "name",
                "",
            )

            results.append(
                f"""
Titre : {title}

Description : {description}

Source : {source}
"""
            )

        return "\n\n".join(results)

    except Exception:
        return None
