from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Sample REST API",
    description="A basic Python REST API built with FastAPI",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# In-memory "database"
# ---------------------------------------------------------------------------
items_db: dict = {
    1: {"id": 1, "name": "Apple", "description": "A fresh red apple", "price": 0.99, "created_at": "2024-01-01T00:00:00"},
    2: {"id": 2, "name": "Banana", "description": "A ripe yellow banana", "price": 0.49, "created_at": "2024-01-01T00:00:00"},
    3: {"id": 3, "name": "Cherry", "description": "Sweet cherries", "price": 2.99, "created_at": "2024-01-01T00:00:00"},
}
next_id = 4

invoices_db: dict = {
    "INV-1001": {
        "id": "INV-1001",
        "vendor": "Acme Supplies",
        "amount": 199.99,
        "currency": "USD",
        "status": "paid",
        "issued_at": "2024-01-15T00:00:00",
        "due_at": "2024-02-14T00:00:00",
    },
    "INV-1002": {
        "id": "INV-1002",
        "vendor": "Globex Corporation",
        "amount": 1249.50,
        "currency": "USD",
        "status": "pending",
        "issued_at": "2024-02-01T00:00:00",
        "due_at": "2024-03-02T00:00:00",
    },
}


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    created_at: str


class Invoice(BaseModel):
    id: str
    vendor: str
    amount: float
    currency: str
    status: str
    issued_at: str
    due_at: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    """Health check / welcome endpoint."""
    return {"message": "Welcome to the Sample REST API!", "status": "ok"}


@app.get("/items", response_model=List[Item], tags=["Items"])
def list_items():
    """Return all items."""
    return list(items_db.values())


@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
def get_item(item_id: int):
    """Return a single item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return items_db[item_id]


@app.get("/invoices", response_model=List[Invoice], tags=["Invoices"])
def list_invoices(
    status: Optional[str] = Query(
        None,
        description="Filter invoices by status (e.g. 'paid', 'pending').",
    ),
):
    """Return all invoices, optionally filtered by status."""
    invoices = list(invoices_db.values())
    if status is not None:
        invoices = [inv for inv in invoices if inv["status"] == status]
    return invoices


@app.get("/invoices/{invoice_id}", response_model=Invoice, tags=["Invoices"])
def get_invoice(invoice_id: str):
    """Return a single invoice by ID."""
    if invoice_id not in invoices_db:
        raise HTTPException(status_code=404, detail=f"Invoice {invoice_id} not found")
    return invoices_db[invoice_id]


@app.post("/items", response_model=Item, status_code=201, tags=["Items"])
def create_item(item: ItemCreate):
    """Create a new item."""
    global next_id
    new_item = {
        "id": next_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "created_at": datetime.utcnow().isoformat(),
    }
    items_db[next_id] = new_item
    next_id += 1
    return new_item


@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item (partial update supported)."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    stored = items_db[item_id]
    update_data = item.model_dump(exclude_unset=True)
    stored.update(update_data)
    return stored


@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted successfully"}
