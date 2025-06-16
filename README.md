## ТЗ LESTA GAMES TF IDF

Чтобы быстрее запустить проект можете открыть **run.bat**
Для запуска через *run.bat* требуеется установленный и
настроенный  **Docker (Docker Desktop)**

*run.bat *начнет билдить докер контейнеры для **frontend** и **backend** части

для *backend* внешний порт подключения будет **8001**
для *frontend* внешний порт подключения будет **3001**

Frontend часть на **Next js**
Backend **Python Fast Api**

если же вы не хотите запускать проект через докер,
то можете настроить проекты отдельно.
Внутри каждой  директории будет пошаговая инструкция

Пример как будет выглядить проекты после билда:

http://localhost:3001 (пустой)
![](https://i.imgur.com/YTIytHI.png)

http://localhost:3001 (после загрузки документов)
![](https://i.imgur.com/An0R7Ux.png)

http://localhost:8001/docs
![](https://i.imgur.com/FUK2jyG.png)

 alembic revision --autogenerate -m "Added account table"
