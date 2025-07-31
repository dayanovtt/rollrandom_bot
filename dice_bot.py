import random
import re
import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from app.token import TOKEN

API_TOKEN = TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание экземпляра бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Функция для обработки команды /roll
async def roll_dice(command: str):
    match = re.match(r"(\d*)d(\d+)(\s*\+(\d+))?", command.strip().lower())
    if match:
        multiplier = int(match.group(1)) if match.group(1) else 1  # Если множитель не указан, по умолчанию 1
        sides = int(match.group(2))  # Количество граней кости
        bonus = int(match.group(4)) if match.group(4) else 0  # Бонус, если он есть

        # Генерация случайных чисел с учетом множителя
        roll_result = [random.randint(1, sides) for _ in range(multiplier)]
        total = sum(roll_result) + bonus
        return f"Roll: {roll_result} (Total: {sum(roll_result)} + Bonus: {bonus} = {total})"
    else:
        return "Некорректная команда. Используй формат 'XdY [+Z]', например '2d20 +3'."


# Создание клавиатуры с кнопками
def get_roll_buttons():
    buttons = [
        [KeyboardButton(text="/r d20+3"), KeyboardButton(text="/r 2d20")],
        [KeyboardButton(text="/r d8"), KeyboardButton(text="/r d8+2"), KeyboardButton(text="/r 1d4")],
        [KeyboardButton(text="/r 1d8"), KeyboardButton(text="/r d20")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


# Обработчик команды /start для показа кнопок
@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        "Выбери одну из команд ниже, или используй команду /r для ввода собственной команды.",
        reply_markup=get_roll_buttons()
    )


# Обработчик команды /r для обработки команд, указанных после команды
@dp.message(Command('r'))
async def cmd_roll(message: Message):
    command = message.text.strip().split(' ', 1)  # Разделяем команду на /r и текст после нее
    if len(command) > 1:
        command = command[1]  # Берем только часть после /r
        result = await roll_dice(command)  # Обрабатываем команду
        await message.reply(result)  # Отправляем результат обратно в тот же чат
    else:
        await message.answer("Пожалуйста, укажи команду для броска, например: /r d20, /r 2d6+3.")


# Обработчик всех текстовых сообщений (не только команды /start)
@dp.message(F.text)  # Фильтруем по типу сообщения - это текст
async def process_message(message: Message):
    command = message.text.strip()

    # Проверяем, если текст соответствует паттерну для броска костей
    if re.match(r"(\d*)d(\d+)(\s*\+(\d+))?", command.lower()):
        result = await roll_dice(command)
        await message.reply(result)  # Используем reply(), чтобы ответить в тот же чат
    else:
        # Если команда не распознана, можно отправить сообщение о некорректной команде
        await message.reply("Некорректная команда. Используй формат '/r XdY[+Z]', например '/r 2d20+3'.")


# Запуск бота
async def main():
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())  # Используем для запуска бота


