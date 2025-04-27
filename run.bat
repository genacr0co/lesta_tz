@echo off
@REM echo Stopping old containers...

@REM docker-compose -f ./lesta_tz_backend/docker-compose.yml down

echo Starting containers...

docker-compose -f ./lesta_tz_backend/docker-compose.yml up --build -d

if %errorlevel% neq 0 (
    echo Error during installation! Exit code: %errorlevel%
    pause
)

@REM echo Project successfully started at http://localhost:8000
pause
