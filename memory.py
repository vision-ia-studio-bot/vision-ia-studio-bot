memory = {}


def save_message(user_id, role, message):
    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append(
        {
            "role": role,
            "content": message,
        }
    )

    memory[user_id] = memory[user_id][-10:]


def get_history(user_id):
    return memory.get(user_id, [])
