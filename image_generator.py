import requests
import urllib.parse


def generate_image(prompt):
    query = urllib.parse.quote(prompt)

    return (
        "https://image.pollinations.ai/prompt/"
        f"{query}"
    )
