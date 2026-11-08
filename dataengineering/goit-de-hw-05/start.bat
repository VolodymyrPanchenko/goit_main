@echo off
setlocal
cd /d "%~dp0"

rem Prefer the project's virtual environment, then Python on PATH.
set "PYTHON=python"
if exist ".venv\Scripts\python.exe" set "PYTHON=%~dp0.venv\Scripts\python.exe"
if exist "venv\Scripts\python.exe" set "PYTHON=%~dp0venv\Scripts\python.exe"

"%PYTHON%" -c "import confluent_kafka" >nul 2>&1
if errorlevel 1 (
    echo Python or confluent-kafka is unavailable.
    echo Activate your Python environment and run: python -m pip install -r requirements.txt
    pause
    exit /b 1
)

start "Sensor processor" cmd /k ""%PYTHON%" -u process_sensors.py"
start "Messages and alerts" cmd /k ""%PYTHON%" -u consumer.py"
start "Sensor producer" cmd /k ""%PYTHON%" -u sensor.py"
endlocal
