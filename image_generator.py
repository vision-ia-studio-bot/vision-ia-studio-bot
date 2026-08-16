import urllib.parse


def generate_image(prompt):
    query = urllib.parse.quote(prompt)

    return (
        f"https://image.pollinations.ai/prompt/{query}"
    )
