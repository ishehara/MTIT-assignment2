# Inventory Management Microservice

Production-ready Inventory Management microservice built with FastAPI and MongoDB (PyMongo), following layered architecture principles.

## Features

- RESTful CRUD API for inventory items
- Layered structure: `controller/`, `service/`, `repository/`, `model/`, `dto/`, `config/`
- MongoDB persistence via PyMongo
- Request validation with Pydantic DTOs
- Global exception handling
- Auto-generated Swagger/OpenAPI docs
- Gateway-friendly routes (`/api/inventory/**`)
- Sample data seeding on startup

## API Endpoints

- `POST /inventory`
- `GET /inventory`
- `GET /inventory/{id}`
- `PUT /inventory/{id}`
- `DELETE /inventory/{id}`

Gateway-compatible duplicates:

- `POST /api/inventory`
- `GET /api/inventory`
- `GET /api/inventory/{id}`
- `PUT /api/inventory/{id}`
- `DELETE /api/inventory/{id}`

## Inventory Item Fields

- `id`
- `name`
- `description`
- `quantity`
- `price`
- `createdAt`

## Run Instructions

1. Move to service directory:

```bash
cd inventory-service
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create environment config:

```bash
copy .env.example .env
```

5. Update MongoDB values in `.env` (`MONGODB_URI`, `MONGODB_DB_NAME`, `INVENTORY_COLLECTION`).

6. Start the service:

```bash
python main.py
```

## Documentation

- Swagger UI: `http://localhost:8003/docs`
- OpenAPI JSON: `http://localhost:8003/openapi.json`

## Health Check

- `GET /health`
