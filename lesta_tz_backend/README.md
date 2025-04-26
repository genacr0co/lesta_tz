## README

### Команды и их описания

1. `python -m venv venv`

   Создает виртуальное окружение с именем `venv` для изоляции проекта от системных библиотек и зависимостей.
2. `source venv/bin/activate` (для Linux) / `venv\Scripts\activate` (для Windows)

   Активирует виртуальное окружение `venv`, позволяя использовать установленные в нем пакеты и избегать конфликтов с глобальными пакетами.
3. `pip install -r requirements.txt`

   Устанавливает зависимости

   <!-- alembic init alembic -->uvicorn src.main:app --reload --reload-dir src --workers 1


   <!-- alembic revision --autogenerate -m "init commit" -->

   <!-- alembic upgrade head -->

   <!-- uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload -->

   <!-- docker-compose up --build -d -->

   <!-- RUNNER_ALLOW_RUNASROOT=true  ./run.sh -->

<!-- 
   curl -X POST -H "Authorization: token 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" \
    https://api.github.com/repos/genacr0co/beerloga-check-list-bot/actions/runs/9177337668/force-cancel -->
