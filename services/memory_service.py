history = {}


def save_message(user_id: int, role: str, text: str) -> None:
    """Сохраняем сообщение пользователя в history"""
    # создаем пользователя, если его нет
    if user_id not in history:
        history[user_id] = []

    # добавляем сообщение в history
    history[user_id].append({
        "role": role,
        "text": text
    })

    # ограничиваем до 20 сообщений (10 пар вопрос-ответ)
    MAX_MESSAGES = 20
    if len(history[user_id]) > MAX_MESSAGES:
        history[user_id] = history[user_id][-MAX_MESSAGES:]


def get_history(user_id: int) -> list:
    """Получаем сообщение пользователя из history по user_id"""
    return history.get(user_id, [])


def clear_history(user_id: int) -> None:
    """Удаляем историю сообщений пользователя из history по user_id"""
    if user_id in history:
        del history[user_id]
