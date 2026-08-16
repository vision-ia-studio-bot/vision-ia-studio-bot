stats = {
    "users": set(),
    "messages": 0,
    "pdfs": 0,
    "web_searches": 0,
}


def add_user(user_id):
    stats["users"].add(user_id)


def count_message():
    stats["messages"] += 1


def count_pdf():
    stats["pdfs"] += 1


def count_web_search():
    stats["web_searches"] += 1


def get_stats():
    return {
        "users": len(stats["users"]),
        "messages": stats["messages"],
        "pdfs": stats["pdfs"],
        "web_searches": stats["web_searches"],
    }
