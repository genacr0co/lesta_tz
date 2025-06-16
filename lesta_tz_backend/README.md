## README

Перед запуском проекта у вас должна быть настроена СУБД `PostgreSQL`

параметры которые используются в проекте для БД:

`DB_HOST = localhost`
`DB_PORT = 5432`
`DB_NAME = tf_idf`
`DB_USER = postgres`
`DB_PASS = postgres`

### Команды и их описания

откройте терминал в директории `/lesta_tz_backend`

1. `python -m venv venv`

   Создает виртуальное окружение с именем `venv` для изоляции проекта от системных библиотек и зависимостей.
2. `source venv/bin/activate` (для Linux) / `venv\Scripts\activate` (для Windows)

   Активирует виртуальное окружение `venv`, позволяя использовать установленные в нем пакеты и избегать конфликтов с глобальными пакетами.
3. `pip install -r requirements.txt`

   Устанавливает зависимости
4. `alembic upgrade head`
   миграции в бд
5. `uvicorn src.main:app --reload`

   запуск проекта
