import os

DB_HOST = str(os.getenv('DB_HOST', 'localhost'))
DB_PORT = str(os.getenv('DB_PORT', '5432'))
DB_NAME = str(os.getenv('DB_NAME', 'tf_idf'))
DB_USER = str(os.getenv('DB_USER', 'postgres'))
DB_PASS = str(os.getenv('DB_PASS', 'postgres'))


SECRET_KEY = str(os.getenv('SECRET_KEY', 'fake25b9bf4a29b0e8525a01b1032d134745fa298ae8b1328f6d0e0180f88fec1a91'))
ALGORITHM = str(os.getenv('ALGORITHM', 'HS256'))
REFRESH_TOKEN_EXPIRE_DAYS = str(os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', '30'))
ACCESS_TOKEN_EXPIRE_MINUTES = str(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))


SMTP_USER = str(os.getenv('SMTP_USER', 'noreply')) 
SMTP_PASSWORD = str(os.getenv('SMTP_PASSWORD', 'admin')) 
SMTP_HOST = str(os.getenv('SMTP_HOST', 'postfix')) 
SMTP_PORT = str(os.getenv('SMTP_PORT', '587')) 
SENDER_EMAIL =  str(os.getenv('SENDER_EMAIL', 'noreply@grenka.uz'))  