# Этап 1: билд-зависимости
FROM python:3.12-slim AS builder

WORKDIR /app

# Установим системные зависимости для сборки некоторых пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Устанавливаем зависимости во временную директорию
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# Этап 2: финальный минимальный образ
FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости из builder-образа
COPY --from=builder /install /usr/local

# wait-for-it + исходный код
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips=*"]
