import os

DB_HOST = os.getenv('DB_HOST', 'localhost')  # Если переменная не задана, используем 'localhost'
DB_PORT = os.getenv('DB_PORT', '5432')  # По умолчанию порт 5432, если не указано
DB_NAME = os.getenv('DB_NAME', 'tf_idf')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')