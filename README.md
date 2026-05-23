# Python REST API Sample

A basic REST API built with **FastAPI** and **Python 3.10+**.

## Features

- Full **CRUD** operations on an `Items` resource
- Auto-generated interactive docs via **Swagger UI** (`/docs`) and **ReDoc** (`/redoc`)
- In-memory data store (easy to swap for a real database)
- Pydantic v2 request/response validation

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/items` | List all items |
| GET | `/items/{id}` | Get item by ID |
| POST | `/items` | Create a new item |
| PUT | `/items/{id}` | Update an item |
| DELETE | `/items/{id}` | Delete an item |

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### 3. Explore the docs

Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Requests

```bash
# List all items
curl http://localhost:8000/items

# Get a single item
curl http://localhost:8000/items/1

# Create an item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Mango", "description": "Tropical fruit", "price": 1.49}'

# Update an item
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 1.25}'

# Delete an item
curl -X DELETE http://localhost:8000/items/1
```
