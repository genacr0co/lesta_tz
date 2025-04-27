# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Теперь копируем весь код проекта
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска (если нужно)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--forwarded-allow-ips=*"]