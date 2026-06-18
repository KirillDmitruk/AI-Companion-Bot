import os

from dotenv import load_dotenv
from google import genai

from services.memory_service import get_history

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

with open("prompt/system.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


def build_contents(system_prompt: str, history: list[dict], user_text: str):
    contents = []

    # system prompt как первое сообщение
    contents.append({
        "role": "user",
        "parts": [{"text": system_prompt}]
    })

    # история
    for msg in history:
        contents.append({
            "role": msg["role"],
            "parts": [{"text": msg["text"]}]
        })

    # текущее сообщение
    contents.append({
        "role": "user",
        "parts": [{"text": user_text}]
    })

    return contents


async def ask_ai(user_id: int, text: str) -> str:
    try:
        history = get_history(user_id)

        contents = build_contents(
            SYSTEM_PROMPT,
            history,
            text
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
        )

        result = response.text
        if result is None:
            return "Я не смог сформировать ответ..."
        return result

    except Exception as e:
        print(f"Ошибка: {e}")

        return (
            "Сейчас AI временно недоступен 🤖\n"
            "Попробуй ещё раз через минуту"
        )
