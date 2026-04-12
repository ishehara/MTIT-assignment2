# Start all backend services in parallel
# Save this script in the root folder and run it: .\START_ALL_SERVICES.ps1

Write-Host "Starting all Backend Services..." -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Start Customer Service (Port 8002)
Write-Host "Starting Customer Service on port 8002..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd 'D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\customer-service'; python -m uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload"

# Start Inventory Service (Port 8003)
Write-Host "Starting Inventory Service on port 8003..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd 'D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\inventory-service'; python -m uvicorn src.main:app --host 0.0.0.0 --port 8003 --reload"

# Start Repair Service (Port 8004)
Write-Host "Starting Repair Service on port 8004..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd 'D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\repair-service'; python -m uvicorn src.main:app --host 0.0.0.0 --port 8004 --reload"

# Start Staff Service (Port 8005)
Write-Host "Starting Staff Service on port 8005..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd 'D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\staff-service'; python -m uvicorn src.main:app --host 0.0.0.0 --port 8005 --reload"

# Start Gateway (Port 8000)
Write-Host "Starting API Gateway on port 8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd 'D:\Y4S2\MTIT\Assignment02\MTIT-assignment2\gateway'; python main.py"

Write-Host "======================================" -ForegroundColor Green
Write-Host "All services are starting..." -ForegroundColor Green
Write-Host "Gateway: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Wait 10 seconds for all services to initialize" -ForegroundColor Green
Start-Sleep -Seconds 10
