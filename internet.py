import requests


def search_web(query):
    try:
        response = requests.get(
            f"https://api.duckduckgo.com/?q={query}&format=json",
            timeout=10,
        )

        data = response.json()

        if data.get("AbstractText"):
            return data["AbstractText"]

        if data.get("Heading"):
            return data["Heading"]

        return "Aucun résultat trouvé."

    except Exception:
        return "La recherche est momentanément indisponible."
