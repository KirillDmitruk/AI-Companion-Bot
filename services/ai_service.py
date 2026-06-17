import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

with open("prompt/prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


async def ask_ai(text: str) -> str:
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {text}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,
    )

    result = response.text
    if result is None:
        return "Я не смог сформировать ответ..."
    return result
