@echo off
REM Start all backend services in parallel
REM Save this file as START_ALL_SERVICES.bat in the root folder

setlocal enabledelayedexpansion

echo.
echo ===============================================
echo Starting all Backend Services...
echo ===============================================
echo.

echo Starting Customer Service on port 8002...
start "Customer Service 8002" cmd /k "cd "D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\customer-service" && python -m uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload"

echo Starting Inventory Service on port 8003...
start "Inventory Service 8003" cmd /k "cd "D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\inventory-service" && python -m uvicorn src.main:app --host 0.0.0.0 --port 8003 --reload"

echo Starting Repair Service on port 8004...
start "Repair Service 8004" cmd /k "cd "D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\repair-service" && python -m uvicorn src.main:app --host 0.0.0.0 --port 8004 --reload"

echo Starting Staff Service on port 8005...
start "Staff Service 8005" cmd /k "cd "D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\staff-service" && python -m uvicorn src.main:app --host 0.0.0.0 --port 8005 --reload"

echo Starting API Gateway on port 8000...
start "API Gateway 8000" cmd /k "cd "D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\gateway" && python main.py"

echo.
echo ===============================================
echo All services starting in separate windows...
echo Wait 10-15 seconds for all to initialize
echo ===============================================
echo.

timeout /t 15
