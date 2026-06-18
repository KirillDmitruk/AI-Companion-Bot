import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram import F
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from services.ai_service import ask_ai
from services.memory_service import save_message

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise ValueError("BOT_TOKEN environment variable not found")

bot = Bot(token=TOKEN)
print(f'Bot = {bot}')
print(f'Bot type = {type(bot)}')
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Hi! I'm your AI Companion bot 🤖")


@dp.message(Command('about'))
async def about_handler(message: Message):
    await message.answer("About")


@dp.message(Command('help'))
async def help_handler(message: Message):
    await message.answer(
        """
    🤖 AI Companion Bot

    Доступные команды:

    /start - запуск бота
    /help - список команд
    /about - информация о боте
    /me - информация о пользователе
    """
    )


@dp.message(Command("me"))
async def me(message: Message):
    user = message.from_user

    if user is None:
        return

    await message.answer(
        f"""
Ваш ID: {user.id}
Ваш username: {user.username}
Ваше имя: {user.first_name}
Ваша фамилия: {user.last_name}
"""
    )

@dp.message(F.text)
async def message_handler(message: Message):
    if not message.text:
        return
    user_id = message.from_user.id
    text = message.text

    # 1. сохраняем user message
    save_message(user_id, "user", text)

    # 2. получаем AI ответ с контекстом
    response = await ask_ai(user_id, text)

    # 3. сохраняем ответ AI
    save_message(user_id, "assistant", response)

    # 4. отправляем пользователю
    await message.answer(response)


@dp.message(F.photo)
async def photo_echo(message: Message):
    await message.answer(f'Ты отправил фото: {message.photo}')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
