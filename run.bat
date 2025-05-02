@echo off

echo Starting Backend containers...

docker-compose -f ./lesta_tz_backend/docker-compose.yml up --build -d

if %errorlevel% neq 0 (
    echo Error during installation! Exit code: %errorlevel%
    pause
)

echo Backend successfully started at http://localhost:8001

echo Starting Frontend containers...

docker-compose -f ./lesta_tz_frontend/docker-compose.yml up --build -d

if %errorlevel% neq 0 (
    echo Error during installation! Exit code: %errorlevel%
    pause
)

echo Frontend successfully started at http://localhost:3001

echo Backend successfully started at http://localhost:8001


pause
