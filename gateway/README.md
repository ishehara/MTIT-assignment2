# Gateway Service Setup

This gateway provides:

- Route forwarding to inventory microservice
- Unified error handling and request logging
- Shared MongoDB connectivity check via `db/mongo.py`

## Files

- `gateway/main.py`: Route paths and request forwarding
- `db/mongo.py`: Shared MongoDB connection and health check
- `gateway/errors.py`: Global exception handlers
- `gateway/middleware.py`: Logging middleware
- `gateway/config.py`: Environment-based configuration

## Environment

1. Copy example env:

```powershell
cd gateway
copy .env.example .env
```

2. In `.env`, set your MongoDB values (do not commit secrets):

- `MONGODB_URI`
- `MONGODB_DB_NAME`

Use your provided Atlas connection string in `MONGODB_URI`.

## Install and Run

```powershell
cd gateway
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## Main Gateway Routes

- Inventory: `/gateway/inventory`, `/gateway/inventory/{item_id}`

## Notes

- The gateway expects downstream services to expose `/api/...` endpoints.
- Update service URLs in `.env` when service ports differ.
