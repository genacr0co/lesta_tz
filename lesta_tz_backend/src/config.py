import os

DB_HOST = str(os.getenv('DB_HOST', 'localhost'))
DB_PORT = str(os.getenv('DB_PORT', '5432'))
DB_NAME = str(os.getenv('DB_NAME', 'tf_idf'))
DB_USER = str(os.getenv('DB_USER', 'postgres'))
DB_PASS = str(os.getenv('DB_PASS', 'postgres'))
