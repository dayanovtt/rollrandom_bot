# Используем официальный Python образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Обновляем pip перед установкой зависимостей
RUN pip install --upgrade pip

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости с подробным выводом
RUN pip install --no-cache-dir -r requirements.txt --verbose

# Копируем весь проект в контейнер
COPY . .

# Команда для запуска бота
CMD ["python", "dice_bot.py"]
