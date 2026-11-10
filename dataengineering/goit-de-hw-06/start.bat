@echo off
rem Usage: start.bat      - one sensor
rem        start.bat 2    - two sensors at the same time
cd /d "%~dp0"

rem Spark Streaming on Windows needs winutils.exe and hadoop.dll in hadoop\bin
rem to write its checkpoint files.
if not exist "%~dp0hadoop\bin\winutils.exe" (
    echo Missing hadoop\bin\winutils.exe - see README, section "Windows setup".
    pause
    exit /b 1
)
set "HADOOP_HOME=%~dp0hadoop"
set "PATH=%~dp0hadoop\bin;%PATH%"
set "PYSPARK_PYTHON=python"
set "PYSPARK_DRIVER_PYTHON=python"

echo Creating Kafka topics...
python create_topic.py
if errorlevel 1 (
    echo Failed to create or check Kafka topics.
    pause
    exit /b 1
)

echo.
echo Starting the alert consumer and Spark processor...
start "Alert consumer" python -u consumer.py
start "Spark processor" cmd /k python -u process_sensors.py

echo.
echo Wait until the Spark window says it is waiting for sensor data.
echo Press any key here to start the sensor producer.
pause > nul

rem Without arguments one sensor starts; with any argument (e.g. "start.bat 2") two.
if "%~1"=="" (
    start "Sensor producer" python -u sensor.py
    echo Sensor producer started in a separate window.
) else (
    start "Sensor producer 1" python -u sensor.py
    start "Sensor producer 2" python -u sensor.py
    echo Two sensor producers started in separate windows.
)
