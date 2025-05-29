# Этап 1: билд-зависимости и установка пакетов
FROM python:3.12-slim AS builder

WORKDIR /app

# Устанавливаем системные зависимости для сборки Python-зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями
COPY requirements.txt .

# Обновляем pip и устанавливаем пакеты в отдельную директорию /install
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# Этап 2: финальный минимальный образ для запуска приложения
FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости из builder-образа
COPY --from=builder /install /usr/local

# Копируем скрипт ожидания и даём ему права на исполнение
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Копируем исходный код
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips=*"]
